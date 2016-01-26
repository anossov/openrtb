# -*- coding: utf-8 -*-

from decimal import Decimal

from . import constants
from .base import Object, Array, String, Field


class Bid(Object):

    u"""At least one bid object is required in a bid set object.

    For each bid, the “nurl” attribute contains the win notice URL.
    If the bidder wins the impression, the exchange calls this notice URL
        a) to inform the bidder of the win and
        b) to convey certain information using substitution macros.

    The “adomain” attribute can be used to check advertiser block list compliance.
    The “iurl” attribute can provide a link to an image that is representative of the campaign’s
    content (irrespective of whether the campaign may have multiple creatives).
    This enables human review for spotting inappropriate content.
    The “cid” attribute can be used to block ads that were previously identified as inappropriate;
    essentially a safety net beyond the block lists.
    The “crid” attribute can be helpful in reporting creative issues back to bidders.
    Finally, the “attr” array indicates the creative attributes that describe the ad to be served.
    """

    #: Bidder generated bid ID to assist with logging/tracking.
    id = Field(String, required=True)

    #: ID of the Imp object in the related bid request.
    impid = Field(String, required=True)

    #: Bid price expressed as CPM although the actual transaction is for a
    #: unit impression only. Note that while the type indicates float, integer
    #: math is highly recommended when handling currencies (e.g., BigDecimal in
    #: Java).
    price = Field(Decimal, required=True)

    #: ID of a preloaded ad to be served if the bid wins.
    adid = Field(String)

    #: Win notice URL called by the exchange if the bid wins; optional means
    #: of serving ad markup.
    nurl = Field(String)

    #: Optional means of conveying ad markup in case the bid wins; supersedes
    #: the win notice if markup is included in both.
    adm = Field(String)

    #: Advertiser domain for block list checking (e.g., “ford.com”). This can
    #: be an array of for the case of rotating creatives. Exchanges can mandate
    #: that only one domain is allowed.
    adomain = Field(Array(String))

    #: Bundle or package name (e.g., com.foo.mygame) of the app being
    #: advertised, if applicable; intended to be a unique ID across exchanges.
    bundle = Field(String)

    #: URL without cache-busting to an image that is representative of the
    #: content of the campaign for ad quality/safety checking.
    iurl = Field(String)

    #: Campaign ID to assist with ad quality checking; the collection of
    #: creatives for which iurl should be representative.
    cid = Field(String)

    #: Creative ID to assist with ad quality checking.
    crid = Field(String)

    #: IAB content categories of the creative. Refer to List 5.1.
    cat = Field(Array(String))

    #: Set of attributes describing the creative. Refer to List 5.3.
    attr = Field(Array(constants.CreativeAttribute))

    #: Reference to the deal.id from the bid request if this bid pertains to a
    #: private marketplace direct deal.
    dealid = Field(String)

    #: Height of the creative in pixels.
    h = Field(int)

    #: Width of the creative in pixels.
    w = Field(int)

    #: Placeholder for bidder-specific extensions to OpenRTB.
    ext = Field(Object)


class SeatBid(Object):

    u"""At least one seatbid object is required in a bid response object.

    A bid response can contain multiple “seatbid” objects, each on behalf of a different bidder seat.
    Since a bid request can include multiple impressions,
    each “seatbid” object can contain multiple bids each pertaining to a different impression on behalf of a seat.
    Thus, each “bid” object must include the impression ID to which it pertains as well as the bid price.
    The “group” attribute can be used to specify if a seat is willing to accept
    any impressions that it can win (default) or if it is only interested
    in winning any if it can win them all (i.e., all or nothing).
    """

    #: Array of 1+ Bid objects (Section 4.2.3) each related to an impression.
    #: Multiple bids can relate to the same impression.
    bid = Field(Array(Bid), required=True)

    #: ID of the bidder seat on whose behalf this bid is made.
    seat = Field(String)

    #: 0 = impressions can be won individually; 1 = impressions must be won or
    #: lost as a group.
    group = Field(int)

    #: Placeholder for bidder-specific extensions to OpenRTB.
    ext = Field(Object)


class BidResponse(Object):

    u"""The top-level bid response object.

    The “id” attribute is a reflection of the bid request ID for logging purposes.
    Similarly, “bidid” is an optional response tracking ID for bidders.
    If specified, it can be included in the subsequent win notice call if the bidder wins.
    At least one “seatbid” object is required, which contains a bid on at least one impression.
    Other attributes are optional since an exchange may establish default values.
    """

    #: ID of the bid request to which this is a response.
    id = Field(String, required=True)

    #: Array of seatbid objects; 1+ required if a bid is to be made.
    seatbid = Field(Array(SeatBid), required=True)

    #: Bidder generated response ID to assist with logging/tracking.
    bidid = Field(String)

    #: Bid currency using ISO-4217 alpha codes.
    cur = Field(String)

    #: Optional feature to allow a bidder to set data in the exchange’s
    #: cookie. The string must be in base85 cookie safe characters and be in any
    #: format. Proper JSON encoding must be used to include “escaped” quotation
    #: marks.
    customdata = Field(String)

    #: Reason for not bidding. Refer to List 5.19.
    nbr = Field(constants.NoBidReason)

    #: Placeholder for bidder-specific extensions to OpenRTB.
    ext = Field(Object)

    @classmethod
    def minimal(cls, id, bid_id, bid_impid, bid_price):
        return cls(id=id, seatbid=[
            SeatBid(bid=[
                Bid(id=bid_id, impid=bid_impid, price=bid_price)
            ])
        ])

    def first_bid(self):
        return self.seatbid[0].bid[0]

    def get_bid_id(self):
        return self.first_bid().id

    def get_imp_id(self):
        return self.first_bid().impid

    def get_ad_id(self):
        return self.first_bid().adid

    def get_first_price(self):
        return self.first_bid().price

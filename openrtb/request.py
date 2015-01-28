# -*- coding: utf-8 -*-
u"""
RTB transactions are initiated when an exchange or other supply source sends a bid request to a bidder.
The bid request consists of a bid request object, at least one impression object,
and may optionally include additional objects providing impression context.
"""

from decimal import Decimal

from . import constants
from .base import Object, Array, String, Field


class Publisher(Object):

    u"""This object describes the publisher of a site or app, depending on which object it is embedded in.

    The publisher object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    """

    #: Exchange-specific publisher ID.
    id = Field(String)

    #: Publisher name (may be aliased at the publisher’s request).
    name = Field(String)

    #: Array of IAB content categories that describe the publisher. Refer to
    #: List 5.1.
    cat = Field(Array(String))

    #: Highest level domain of the publisher (e.g., “publisher.com”).
    domain = Field(String)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Producer(Object):

    u"""This object describes the content of a site or app, depending on which object its parent is embedded in.

    The producer is useful when content where the ad is shown is syndicated,
    and may appear on a completely different publisher.
    The producer object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    This object is optional, but useful if the content producer is different from the site publisher.
    """

    #: Content producer or originator ID. Useful if content is syndicated and
    #: may be posted on a site using embed tags.
    id = Field(String)

    #: Content producer or originator name (e.g., “Warner Bros”).
    name = Field(String)

    #: Array of IAB content categories that describe the content producer.
    #: Refer to List 5.1.
    cat = Field(Array(String))

    #: Highest level domain of the content producer (e.g., “producer.com”).
    domain = Field(String)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Geo(Object):

    u"""Depending on the parent object, this object describes the current geographic location of the device, or it may describe the home geo of the user.

    The geo object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    Note that the Geo Object may appear in one or both the Device Object and the User Object.
    This is intentional, since the information may be derived from either a device-oriented
    source (such as IP geo lookup), or by user registration information (for example
    provided to a publisher through a user registration).
    If the information is in conflict, it’s up to the bidder to determine which information to use.
    """

    #: Latitude from -90.0 to +90.0, where negative is south
    lat = Field(float)

    #: Longitude from -180.0 to +180.0, where negative is west.
    lon = Field(float)

    #: Source of location data; recommended when passing lat/lon. Refer to
    #: List 5.16.
    type = Field(constants.LocationType)

    #: Country code using ISO-3166-1-alpha-3.
    country = Field(String)

    #: Region code using ISO-3166-2; 2-letter state code if USA.
    region = Field(String)

    #: Region of a country using FIPS 10-4 notation. While OpenRTB supports
    #: this attribute, it has been withdrawn by NIST in 2008.
    regionfips104 = Field(String)

    #: Google metro code; similar to but not exactly Nielsen DMAs. See
    #: Appendix A for a link to the codes.
    metro = Field(String)

    #: City using United Nations Code for Trade & Transport Locations. See
    #: Appendix A for a link to the codes.
    city = Field(String)

    #: Zip or postal code.
    zip = Field(String)

    #: Local device time as the number +/- of minutes from UTC.
    utcoffset = Field(int)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)

    def loc(self):
        if self.lat and self.lon:
            return self.lat, self.lon


class Segment(Object):

    u"""The segment object is a child of the data object, and describes data segments applicable to the user for the given data provider.

    The data and segment objects together allow data about the user to be passed to bidders in the bid request.
    Segment objects convey specific units of information from the provider identified in the parent data object.
    The segment object itself and all of its parameters are optional, so default values are not provided;
    if an optional parameter is not specified, it should be considered unknown.
    """

    #: ID of the data segment specific to the data provider.
    id = Field(String)

    #: Name of the data segment specific to the data provider.
    name = Field(String)

    #: String representation of the data segment value.
    value = Field(String)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Data(Object):

    u"""The data object is a child of the user object and describes a data source.
    Once segment objects are embedded, data about the user may be passed to bidders.

    The data and segment objects together allow data about the user to be passed to bidders in the bid request.
    This data may be from multiple sources (e.g., the exchange itself, third party providers)
    as specified by the data object ID field. A bid request can mix data objects from multiple providers.
    The data object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    """

    #: Exchange-specific ID for the data provider.
    id = Field(String)

    #: Exchange-specific name for the data provider.
    name = Field(String)

    #: Array of Segment (Section 3.2.15) objects that contain the actual data
    #: values.
    segment = Field(Array(Segment))

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class User(Object):

    u"""This object describes the user, and may include unique identifiers for the user.

    The “user” object contains information known or derived about the human user of the device.
    Note that the user ID is an exchange artifact (refer to the “device” object for hardware or platform derived IDs)
    and may be subject to rotation policies.
    However, this user ID must be stable long enough to serve reasonably as the basis for frequency capping.
    The user object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    If device ID is used as a proxy for unique user ID, use the device object.
    """

    #: Exchange-specific ID for the user. At least one of id or buyerid is
    #: recommended.
    id = Field(String)

    #: Buyer-specific ID for the user as mapped by the exchange for the buyer.
    #: At least one of buyerid or id is recommended.
    buyerid = Field(String)

    #: Year of birth as a 4-digit integer.
    yob = Field(int)

    #: Gender, where “M” = male, “F” = female, “O” = known to be other (i.e.,
    #: omitted is unknown).
    gender = Field(String)

    #: Comma separated list of keywords, interests, or intent.
    keywords = Field(String)

    #: Optional feature to pass bidder data that was set in the exchange’s
    #: cookie. The string must be in base85 cookie safe characters and be in any
    #: format. Proper JSON encoding must be used to include “escaped” quotation
    #: marks.
    customdata = Field(String)

    #: Location of the user’s home base defined by a Geo object (Section
    #: 3.2.12). This is not necessarily their current location.
    geo = Field(Geo)

    #: Additional user data. Each Data object (Section 3.2.14) represents a
    #: different data source.
    data = Field(Array(Data))

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Device(Object):

    u"""This object describes the device the ad impression will be delivered to and its capabilities.

    The “device” object provides information pertaining to the device including
    its hardware, platform, location, and carrier.
    This device can refer to a mobile handset, a desktop computer, set top box or other digital device.
    The device object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    In general, the most essential fields are either the IP address (to enable geo-lookup for the bidder),
    or providing geo information directly in the geo object.
    """

    #: Browser user agent string.
    ua = Field(String)

    #: Location of the device assumed to be the user’s current location
    #: defined by a Geo object (Section 3.2.12).
    geo = Field(Geo)

    #: Standard “Do Not Track” flag as set in the header by the browser, where
    #: 0 = tracking is unrestricted, 1 = do not track.
    dnt = Field(int)

    #: “Limit Ad Tracking” signal commercially endorsed (e.g., iOS, Android),
    #: where 0 = tracking is unrestricted, 1 = tracking must be limited per
    #: commercial guidelines.
    lmt = Field(int)

    #: IPv4 address closest to device.
    ip = Field(String)

    #: IP address closest to device as IPv6.
    ipv6 = Field(String)

    #: The general type of device. Refer to List 5.17.
    devicetype = Field(constants.DeviceType)

    #: Device make (e.g., “Apple”).
    make = Field(String)

    #: Device model (e.g., “iPhone”).
    model = Field(String)

    #: Device operating system (e.g., “iOS”).
    os = Field(String)

    #: Device operating system version (e.g., “3.1.2”).
    osv = Field(String)

    #: Hardware version of the device (e.g., “5S” for iPhone 5S).
    hwv = Field(String)

    #: Physical height of the screen in pixels.
    h = Field(int)

    #: Physical width of the screen in pixels.
    w = Field(int)

    #: Screen size as pixels per linear inch.
    ppi = Field(int)

    #: The ratio of physical pixels to device independent pixels.
    pxratio = Field(float)

    #: Support for JavaScript, where 0 = no, 1 = yes.
    js = Field(int)

    #: Version of Flash supported by the browser.
    flashver = Field(String)

    #: Browser language using ISO-639-1-alpha-2.
    language = Field(String)

    #: Carrier or ISP (e.g., “VERIZON”). “WIFI” is often used in mobile to
    #: indicate high bandwidth (e.g., video friendly vs. cellular).
    carrier = Field(String)

    #: Network connection type. Refer to List 5.18.
    connectiontype = Field(constants.ConnectionType)

    #: ID sanctioned for advertiser use in the clear (i.e., not hashed).
    ifa = Field(String)

    #: Hardware device ID (e.g., IMEI); hashed via SHA1.
    didsha1 = Field(String)

    #: Hardware device ID (e.g., IMEI); hashed via MD5.
    didmd5 = Field(String)

    #: Platform device ID (e.g., Android ID); hashed via SHA1.
    dpidsha1 = Field(String)

    #: Platform device ID (e.g., Android ID); hashed via MD5.
    dpidmd5 = Field(String)

    #: MAC address of the device; hashed via SHA1.
    macsha1 = Field(String)

    #: MAC address of the device; hashed via MD5.
    macmd5 = Field(String)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)

    def get_geo(self):
        return self.geo or Geo()

    def is_on_cellular(self):
        return self.connectiontype and self.connectiontype.is_cellular()


class Content(Object):

    u"""This object describes the content of a site or app, depending on which object it is embedded in.

    The content object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    This object describes the content in which the impression will appear (may be syndicated or non-syndicated content).
    This object may be useful in the situation where syndicated content contains impressions
    and does not necessarily match the publisher’s general content.
    The exchange might or might not have knowledge of the page where the content is running,
    as a result of the syndication method.
    (For example, video impressions embedded in an iframe on an unknown web property or device.)
    """

    #: ID uniquely identifying the content.
    id = Field(String)

    #: Episode number (typically applies to video content).
    episode = Field(int)

    #: Content title.
    #: Video Examples: “Search Committee” (television), “A New Hope” (movie),
    #    or “Endgame” (made for web).
    #: Non-Video Example: “Why an Antarctic Glacier Is Melting So Quickly”
    #    (Time magazine article).
    title = Field(String)

    #: Content series.
    #: Video Examples: “The Office” (television), “Star Wars” (movie), or
    #    “Arby ‘N’ The Chief” (made for web).
    #: Non-Video Example: “Ecocentric” (Time Magazine blog).
    series = Field(String)

    #: Content season; typically for video content (e.g., “Season 3”).
    season = Field(String)

    #: Details about the content Producer (Section 3.2.10).
    producer = Field(Producer)

    #: URL of the content, for buy-side contextualization or review.
    url = Field(String)

    #: Array of IAB content categories that describe the content producer.
    #: Refer to List 5.1.
    cat = Field(Array(String))

    #: Video quality per IAB’s classification. Refer to List 5.11.
    videoquality = Field(constants.VideoQuality)

    #: Type of content (game, video, text, etc.). Refer to List 5.14.
    context = Field(String)

    #: Content rating (e.g., MPAA).
    contentrating = Field(String)

    #: User rating of the content (e.g., number of stars, likes, etc.).
    userrating = Field(String)

    #: Media rating per QAG guidelines. Refer to List 5.15.
    qagmediarating = Field(constants.QAGMediaRating)

    #: Comma separated list of keywords describing the content.
    keywords = Field(String)

    #: 0 = not live, 1 = content is live (e.g., stream, live blog).
    livestream = Field(int)

    #: 0 = indirect, 1 = direct.
    sourcerelationship = Field(int)

    #: Length of content in seconds; appropriate for video or audio.
    len = Field(int)

    #: Content language using ISO-639-1-alpha-2.
    language = Field(String)

    #: Indicator of whether or not the content is embeddable (e.g., an
    #: embeddable video player), where 0 = no, 1 = yes.
    embeddable = Field(int)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Site(Object):

    u"""Either a site or app object may be included – not both. Neither is required.

    A site object should be included if the ad supported content is part of a website (as opposed to an application).
    A bid request must not contain both a site object and an app object.
    The site object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    At a minimum, it’s useful to provide a page URL or a site ID, but this is not strictly required.
    """

    #: Exchange-specific site ID.
    id = Field(String)

    #: Site name (may be aliased at the publisher’s request).
    name = Field(String)

    #: Domain of the site (e.g., “mysite.foo.com”).
    domain = Field(String)

    #: Array of IAB content categories of the site. Refer to List 5.1.
    cat = Field(Array(String))

    #: Array of IAB content categories that describe the current section of
    #: the site. Refer to List 5.1.
    sectioncat = Field(Array(String))

    #: Array of IAB content categories that describe the current page or view
    #: of the site. Refer to List 5.1.
    pagecat = Field(Array(String))

    #: URL of the page where the impression will be shown.
    page = Field(String)

    #: Referrer URL that caused navigation to the current page.
    ref = Field(String)

    #: Search string that caused navigation to the current page.
    search = Field(String)

    #: Mobile-optimized signal, where 0 = no, 1 = yes.
    movile = Field(int)

    #: Indicates if the site has a privacy policy, where 0 = no, 1 = yes.
    privacypolicy = Field(int)

    #: Details about the Publisher (Section 3.2.8) of the site.
    publisher = Field(Publisher)

    #: Details about the Content (Section 3.2.9) within the site.
    content = Field(Content)

    #: Comma separated list of keywords about the site.
    keywords = Field(String)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class App(Object):

    u"""Either a site or app object may be included – not both. Neither is required.

    An “app” object should be included if the ad supported content is part of a mobile
    application (as opposed to a mobile website).
    A bid request must not contain both an “app” object and a “site” object.
    The app object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    At a minimum, it’s useful to provide an App ID or bundle, but this is not strictly required.
    """

    #: Exchange-specific app ID.
    id = Field(String)

    #: App name (may be aliased at the publisher’s request).
    name = Field(String)

    #: Application bundle or package name (e.g., com.foo.mygame); intended to
    #: be a unique ID across exchanges.
    bundle = Field(String)

    #: Domain of the app (e.g., “mygame.foo.com”).
    domain = Field(String)

    #: App store URL for an installed app; for QAG 1.5 compliance.
    storeurl = Field(String)

    #: Array of IAB content categories of the app. Refer to List 5.1.
    cat = Field(Array(String))

    #: Array of IAB content categories that describe the current section of
    #: the app. Refer to List 5.1.
    sectioncat = Field(Array(String))

    #: Array of IAB content categories that describe the current page or view
    #: of the app. Refer to List 5.1.
    pagecat = Field(Array(String))

    #: Application version.
    ver = Field(String)

    #: Indicates if the app has a privacy policy, where 0 = no, 1 = yes.
    privacypolicy = Field(int)

    #: 0 = app is free, 1 = the app is a paid version.
    paid = Field(int)

    #: Details about the Publisher (Section 3.2.8) of the app.
    publisher = Field(Publisher)

    #: Details about the Content (Section 3.2.9) within the app.
    content = Field(Content)

    #: Comma separated list of keywords about the app.
    keywords = Field(String)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Banner(Object):

    u"""A banner object typically describes an ad opportunity for banner, rich media or in-banner video inventory.

    The “banner” object must be included directly in the impression object
    if the impression offered for auction is display or rich media,
    or it may be optionally embedded in the video object to describe
    the companion banners available for the linear or non-linear video ad.
    The banner object may include a unique identifier; this can be useful
    if these IDs can be leveraged in the VAST response
    to dictate placement of the companion creatives when multiple
    companion ad opportunities of the same size are available on a page.
    """

    #: Width of the impression in pixels.
    #: If neither wmin nor wmax are specified, this value is an exact width
    #: requirement. Otherwise it is a preferred width.
    w = Field(int)

    #: Height of the impression in pixels.
    #: If neither hmin nor hmax are specified, this value is an exact height
    #: requirement. Otherwise it is a preferred height.
    h = Field(int)

    #: Maximum width of the impression in pixels.
    #: If included along with a w value then w should be interpreted as a
    #: recommended or preferred width.
    wmax = Field(int)

    #: Maximum height of the impression in pixels.
    #: If included along with an h value then h should be interpreted as a
    #: recommended or preferred height.
    hmax = Field(int)

    #: Minimum width of the impression in pixels.
    #: If included along with a w value then w should be interpreted as a
    #: recommended or preferred width.
    wmin = Field(int)

    #: Minimum height of the impression in pixels.
    #: If included along with an h value then h should be interpreted as a
    #: recommended or preferred height.
    hmin = Field(int)

    #: Unique identifier for this banner object. Recommended when Banner
    #: objects are used with a Video object (Section 3.2.4) to represent an
    #: array of companion ads. Values usually start at 1 and increase with each
    #: object; should be unique within an impression.
    id = Field(String)

    #: Blocked banner ad types. Refer to List 5.2.
    btype = Field(Array(constants.BannerType))

    #: Blocked creative attributes. Refer to List 5.3.
    battr = Field(Array(constants.CreativeAttribute))

    #: Ad position on screen. Refer to List 5.4.
    pos = Field(constants.AdPosition)

    #: Content MIME types supported. Popular MIME types may include
    #“application/x-shockwave-flash”, “image/jpg”, and “image/gif”.
    mimes = Field(Array(String))

    #: Indicates if the banner is in the top frame as opposed to an iframe,
    #: where 0 = no, 1 = yes.
    topframe = Field(int)

    #: Directions in which the banner may expand. Refer to List 5.5.
    expdir = Field(Array(constants.ExpandableDirection))

    #: List of supported API frameworks for this impression. Refer to List
    #: 5.6. If an API is not explicitly listed, it is assumed not to be
    #: supported.
    api = Field(Array(constants.APIFramework))

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)

    def blocked_types(self):
        return set(self.btype or [])

    def size(self):
        if self.w and self.h:
            return self.w, self.h


class Video(Object):

    u"""A video object typically describes an ad opportunity for in-stream video inventory.

    The “video” object must be included directly in the impression object if the impression offered
    for auction is an in-stream video ad opportunity.
    Note that for the video object, many of the fields are non-essential for a minimally viable exchange interfaces.
    These parameters do not necessarily need to be specified to the bidder,
    if they are always the same for all impression,
    or if the exchange chooses not to supply the additional information to the bidder.
    """

    #: Content MIME types supported. Popular MIME types may include
    #: “video/x-ms-wmv” for Windows Media and “video/x-flv” for Flash Video.
    mimes = Field(Array(String), required=True)

    #: Minimum video ad duration in seconds.
    minduration = Field(int, required=True)

    #: Maximum video ad duration in seconds.
    maxduration = Field(int, required=True)

    #: NOTE: Use of protocols instead is highly recommended.
    #: Supported video bid response protocol. Refer to List 5.8. At least one
    #: supported protocol must be specified in either the protocol or protocols
    #: attribute.
    protocol = Field(constants.VideoProtocol)

    #: Array of supported video bid response protocols. Refer to List 5.8. At
    #: least one supported protocol must be specified in either the protocol or
    #: protocols attribute.
    protocols = Field(Array(constants.VideoProtocol))

    #: Width of the video player in pixels.
    w = Field(int)

    #: Height of the video player in pixels.
    h = Field(int)

    #: Indicates the start delay in seconds for pre-roll, mid-roll, or post-
    #: roll ad placements. Refer to List 5.10 for additional generic values.
    startdelay = Field(int)

    #: Indicates if the impression must be linear, nonlinear, etc. If none
    #: specified, assume all are allowed. Refer to List 5.7.
    linearity = Field(constants.VideoLinearity, required=True)

    #: If multiple ad impressions are offered in the same bid request, the
    #: sequence number will allow for the coordinated delivery of multiple
    #: creatives.
    sequence = Field(int, default=1)

    #: Blocked creative attributes. Refer to List 5.3.
    battr = Field(Array(constants.CreativeAttribute))

    #: Maximum extended video ad duration if extension is allowed. If blank or
    #: 0, extension is not allowed. If -1, extension is allowed, and there is no
    #: time limit imposed. If greater than 0, then the value represents the
    #: number of seconds of extended play supported beyond the maxduration
    #: value.
    maxextended = Field(int)

    #: Minimum bit rate in Kbps. Exchange may set this dynamically or
    #: universally across their set of publishers.
    minbitrate = Field(int)

    #: Maximum bit rate in Kbps. Exchange may set this dynamically or
    #: universally across their set of publishers.
    maxbitrate = Field(int)

    #: Indicates if letter-boxing of 4:3 content into a 16:9 window is
    #    allowed, where 0 = no, 1 = yes.
    boxingallowed = Field(int, default=1)

    #: Allowed playback methods. If none specified, assume all are allowed.
    #: Refer to List 5.9.
    playbackmethod = Field(Array(constants.VideoPlaybackMethod))

    #: Supported delivery methods (e.g., streaming, progressive). If none
    #: specified, assume all are supported. Refer to List 5.13.
    delivery = Field(Array(constants.ContentDeliveryMethod))

    #: Ad position on screen. Refer to List 5.4.
    pos = Field(constants.AdPosition)

    #: Array of Banner objects (Section 3.2.3) if companion ads are available.
    companionad = Field(Array(Banner))

    #: List of supported API frameworks for this impression. Refer to List
    #: 5.6. If an API is not explicitly listed, it is assumed not to be
    #: supported.
    api = Field(Array(constants.APIFramework))

    #: Supported VAST companion ad types. Refer to List 5.12. Recommended if
    #: companion Banner objects are included via the companionad array.
    companiontype = Field(Array(constants.CompanionType))

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Native(Object):

    u"""
    A “native” object represents a native type impression. Native ad units are
    intended to blend seamlessly into the surrounding content (e.g., a
    sponsored Twitter or Facebook post). As such, the response must be well-
    structured to afford the publisher fine-grained control over rendering.

    The Native Subcommittee has developed a companion specification to OpenRTB
    called the Native Ad Specification. It defines the request parameters and
    response markup structure of native ad units. This object provides the
    means of transporting request parameters as an opaque string so that the
    specific parameters can evolve separately under the auspices of the Native
    Ad Specification. Similarly, the ad markup served will be structured
    according to that specification.

    The presence of a Native as a subordinate of the Imp object indicates that
    this impression is offered as a native type impression. At the publisher’s
    discretion, that same impression may also be offered as banner and/or video
    by also including as Imp subordinates the Banner and/or Video objects,
    respectively. However, any given bid for the impression must conform to one
    of the offered types.
    """

    #: Request payload complying with the Native Ad Specification.
    request = Field(String, required=True)

    #: Version of the Native Ad Specification to which request complies;
    #: highly recommended for efficient parsing.
    ver = Field(String)

    #: List of supported API frameworks for this impression. Refer to List
    #: 5.6. If an API is not explicitly listed, it is assumed not to be
    #: supported.
    api = Field(Array(int))

    #: Blocked creative attributes. Refer to List 5.3.
    battr = Field(Array(int))

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Deal(Object):

    u"""A “deal” object constitutes a deal struck a priori between a buyer and a seller.

    A “deal” object constitutes a deal struck a priori between a buyer and a seller and indicates that
    this impression is available under the terms of that deal.
    """

    #: A unique identifier for the direct deal.
    id = Field(String, required=True)

    #: Minimum bid for this impression expressed in CPM.
    bidfloor = Field(float)

    #: Currency specified using ISO-4217 alpha codes. This may be different
    #: from bid currency returned by bidder if this is allowed by the exchange.
    bidfloorcur = Field(String, default='USD')

    #: Optional override of the overall auction type of the bid request, where
    #: 1 = First Price, 2 = Second Price Plus, 3 = the value passed in bidfloor
    #: is the agreed upon deal price. Additional auction types can be defined by
    #: the exchange.
    at = Field(constants.AuctionType)

    #: Whitelist of buyer seats allowed to bid on this deal. Seat IDs must be
    #: communicated between bidders and the exchange a priori. Omission implies
    #: no seat restrictions.
    wseat = Field(Array(String))

    #: Array of advertiser domains (e.g., advertiser.com) allowed to bid on
    #: this deal. Omission implies no advertiser restrictions.
    wadomain = Field(Array(String))

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class PMP(Object):

    u"""Top-level object for Direct Deals

    The “pmp” object contains a parent object for usage within the context of private marketplaces
    and the use of the RTB protocol to execute Direct Deals.
    """

    #: Indicator of auction eligibility to seats named in the Direct Deals
    #: object, where 0 = all bids are accepted, 1 = bids are restricted to the
    #: deals specified and the terms thereof.
    private_auction = Field(int)

    #: Array of Deal (Section 3.2.18) objects that convey the specific deals
    #: applicable to this impression.
    deals = Field(Array(Deal))

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Impression(Object):

    u"""At least one impression object is required in a bid request object.

    The “imp” object desribes the ad position or impression being auctioned.
    A single bid request can include multiple “imp” objects,
    a use case for which might be an exchange that supports selling all ad positions on a given page as a bundle.
    Each “imp” object has a required ID so that bids can reference them individually.
    """

    #: A unique identifier for this impression within the context of the bid
    #    request (typically, starts with 1 and increments.
    id = Field(String, required=True)

    #: A Banner object (Section 3.2.3); required if this impression is offered
    #: as a banner ad opportunity.
    banner = Field(Banner)

    #: A Video object (Section 3.2.4); required if this impression is offered
    #: as a video ad opportunity.
    video = Field(Video)

    #: A Native object (Section 3.2.5); required if this impression is offered
    #: as a native ad opportunity.
    native = Field(Native)

    #: Name of ad mediation partner, SDK technology, or player responsible for
    #: rendering ad (typically video or mobile). Used by some ad servers to
    #: customize ad code by partner. Recommended for video and/or apps.
    displaymanager = Field(String)

    #: Version of ad mediation partner, SDK technology, or player responsible
    #: for rendering ad (typically video or mobile). Used by some ad servers to
    #: customize ad code by partner. Recommended for video and/or apps.
    displaymanagerver = Field(String)

    #: 1 = the ad is interstitial or full screen, 0 = not interstitial.
    instl = Field(int)

    #: Identifier for specific ad placement or ad tag that was used to
    #: initiate the auction. This can be useful for debugging of any issues, or
    #: for optimization by the buyer.
    tagid = Field(String)

    #: Minimum bid for this impression expressed in CPM.
    bidfloor = Field(Decimal)

    #: Currency specified using ISO-4217 alpha codes. This may be different
    #: from bid currency returned by bidder if this is allowed by the exchange.
    bidfloorcur = Field(String, default='USD')

    #: Flag to indicate if the impression requires secure HTTPS URL creative
    #: assets and markup, where 0 = non-secure, 1 = secure. If omitted, the
    #: secure state is unknown, but non-secure HTTP support can be assumed.
    secure = Field(int)

    #: Array of exchange-specific names of supported iframe busters.
    iframebuster = Field(Array(String))

    #: A Pmp object (Section 3.2.17) containing any private marketplace deals
    #: in effect for this impression.
    pmp = Field(PMP)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class Regulations(Object):

    u"""The “regs” object contains any legal, governmental, or industry regulations that apply to the request.

    The first regulation added signal whether or not the request falls under the United States
    Federal Trade Commission’s regulations for the United States Children’s Online Privacy
    Protection Act (“COPPA”). See the COPPA appendix for details.
    The regs object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    """

    #: Flag indicating if this request is subject to the COPPA regulations
    #    established by the USA FTC, where 0 = no, 1 = yes.
    coppa = Field(int)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)


class BidRequest(Object):

    u"""Top-level bid request object.

    The top-level bid request object contains a globally unique bid request or auction ID.
    This “id” attribute is required as is at least one “imp” (i.e., impression) object.
    Other attributes are optional since an exchange may establish default values.
    """

    #: Unique ID of the bid request, provided by the exchange.
    id = Field(String, required=True)

    #: Array of Imp objects (Section 3.2.2) representing the
    #: impressionsoffered. Atleast1Impobjectisrequired.
    imp = Field(Array(Impression), required=True)

    #: Details via a Site object (Section 3.2.6) about the publisher’s
    #: website. Only applicable and recommended for websites.
    site = Field(Site)

    #: Details via an App object (Section 3.2.7) about the publisher’s app
    #: (i.e., non-browser applications). Only applicable and recommended for
    #: apps.
    app = Field(App)

    #: Details via a Device object (Section 3.2.11) about the user’s device to
    #: which the impression will be delivered.
    device = Field(Device)

    #: Details via a User object (Section 3.2.13) about the human user of the
    #: device; the advertising audience.
    user = Field(User)

    #: Indicator of test mode in which auctions are not billable, where 0 =
    #: live mode, 1 = test mode.
    test = Field(int)

    #: Auction type, where 1 = First Price, 2 = Second Price Plus. Exchange-
    #: specific auction types can be defined using values greater than 500.
    at = Field(constants.AuctionType, default=constants.AuctionType.SECOND_PRICE)

    #: Maximum time in milliseconds to submit a bid to avoid timeout. This
    #: value is commonly communicated offline.
    tmax = Field(int)

    #: Whitelist of buyer seats allowed to bid on this impression. Seat IDs
    #: must be communicated between bidders and the exchange a priori. Omission
    #: implies no seat restrictions.
    wseat = Field(Array(String))

    #: Flag to indicate if Exchange can verify that the impressions offered
    #: represent all of the impressions available in context (e.g., all on the
    #: web page, all video spots such as pre/mid/post roll) to support road-
    #: blocking. 0 = no or unknown, 1 = yes, the impressions offered represent
    #: all that are available.
    allimps = Field(int)

    #: Array of allowed currencies for bids on this bid request using ISO-4217
    #: alpha codes. Recommended only if the exchange accepts multiple
    #: currencies.
    cur = Field(Array(String))

    #: Blocked advertiser categories using the IAB content categories. Refer
    #: to List 5.1.
    bcat = Field(Array(String))

    #: Block list of advertisers by their domains (e.g., “ford.com”).
    badv = Field(Array(String))

    #: A Regs object (Section 3.2.16) that specifies any industry, legal, or
    #: governmental regulations in force for this request.
    regs = Field(Regulations)

    #: Placeholder for exchange-specific extensions to OpenRTB.
    ext = Field(Object)

    def get_app(self):
        return self.app or App()

    def get_site(self):
        return self.site or Site()

    def get_device(self):
        return self.device or Device()

    def get_user(self):
        return self.user or User()

    @staticmethod
    def minimal(id, imp_id):
        return BidRequest(id=id, imp=[Impression(id=imp_id, banner=Banner())])

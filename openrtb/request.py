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

    id = Field(String)
    name = Field(String)
    cat = Field(Array(String))
    domain = Field(String)
    ext = Field(Object)


class Producer(Object):
    u"""This object describes the content of a site or app, depending on which object its parent is embedded in.

    The producer is useful when content where the ad is shown is syndicated,
    and may appear on a completely different publisher.
    The producer object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    This object is optional, but useful if the content producer is different from the site publisher.
    """

    id = Field(String)
    name = Field(String)
    cat = Field(Array(String))
    domain = Field(String)
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

    lat = Field(float)
    lon = Field(float)
    country = Field(String)
    region = Field(String)
    regionfips104 = Field(String)
    metro = Field(String)
    city = Field(String)
    zip = Field(String)
    type = Field(constants.LocationType)
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

    id = Field(String)
    name = Field(String)
    value = Field(String)
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

    id = Field(String)
    name = Field(String)
    segment = Field(Array(Segment))
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

    id = Field(String)
    buyerid = Field(String)
    yob = Field(int)
    gender = Field(String)
    keywords = Field(String)
    customdata = Field(String)
    geo = Field(Geo)
    data = Field(Array(Data))
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

    dnt = Field(int)
    ua = Field(String)
    ip = Field(String)
    geo = Field(Geo)
    didsha1 = Field(String)
    didmd5 = Field(String)
    dpidsha1 = Field(String)
    dpidmd5 = Field(String)
    macsha1 = Field(String)
    macmd5 = Field(String)
    ipv6 = Field(String)
    carrier = Field(String)
    language = Field(String)
    make = Field(String)
    model = Field(String)
    os = Field(String)
    osv = Field(String)
    js = Field(int)
    connectiontype = Field(constants.ConnectionType)
    devicetype = Field(constants.DeviceType)
    flashver = Field(String)
    ifa = Field(String)
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

    id = Field(String)
    episode = Field(int)
    title = Field(String)
    series = Field(String)
    season = Field(String)
    url = Field(String)
    cat = Field(Array(String))
    videoquality = Field(constants.VideoQuality)
    keywords = Field(String)
    contentrating = Field(String)
    userrating = Field(String)
    context = Field(String)
    livestream = Field(int)
    sourcerelationship = Field(int)
    producer = Field(Producer)
    len = Field(int)
    qagmediarating = Field(constants.QAGMediaRating)
    embeddable = Field(int)
    language = Field(String)
    ext = Field(Object)


class Site(Object):
    u"""Either a site or app object may be included – not both. Neither is required.

    A site object should be included if the ad supported content is part of a website (as opposed to an application).
    A bid request must not contain both a site object and an app object.
    The site object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    At a minimum, it’s useful to provide a page URL or a site ID, but this is not strictly required.
    """

    id = Field(String)
    name = Field(String)
    domain = Field(String)
    cat = Field(Array(String))
    sectioncat = Field(Array(String))
    pagecat = Field(Array(String))
    page = Field(String)
    privacypolicy = Field(int)
    ref = Field(String)
    search = Field(String)
    publisher = Field(Publisher)
    content = Field(Content)
    keywords = Field(String)
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

    id = Field(String)
    name = Field(String)
    domain = Field(String)
    cat = Field(Array(String))
    sectioncat = Field(Array(String))
    pagecat = Field(Array(String))
    ver = Field(String)
    bundle = Field(String)
    privacypolicy = Field(int)
    paid = Field(int)
    publisher = Field(Publisher)
    content = Field(Content)
    keywords = Field(String)
    storeurl = Field(String)
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

    w = Field(int)
    h = Field(int)
    wmax = Field(int)
    hmax = Field(int)
    wmin = Field(int)
    hmin = Field(int)
    id = Field(String)
    pos = Field(constants.AdPosition)
    btype = Field(Array(constants.BannerType))
    battr = Field(Array(constants.CreativeAttribute))
    mimes = Field(Array(String))
    topframe = Field(int)
    expdir = Field(Array(constants.ExpandableDirection))
    api = Field(Array(constants.APIFramework))
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

    mimes = Field(Array(String), required=True)
    linearity = Field(constants.VideoLinearity, required=True)
    minduration = Field(int, required=True)
    maxduration = Field(int, required=True)
    protocol = Field(constants.VideoProtocol)
    protocols = Field(Array(constants.VideoProtocol))
    w = Field(int)
    h = Field(int)
    startdelay = Field(int)
    sequence = Field(int, 1)
    battr = Field(Array(constants.CreativeAttribute))
    maxextended = Field(int)
    minbitrate = Field(int)
    maxbitrate = Field(int)
    boxingallowed = Field(int, 1)
    playbackmethod = Field(Array(constants.VideoPlaybackMethod))
    delivery = Field(Array(constants.ContentDeliveryMethod))
    pos = Field(constants.AdPosition)
    companionad = Field(Array(Banner))
    companiontype = Field(Array(constants.CompanionType))
    api = Field(Array(constants.APIFramework))
    ext = Field(Object)


class Deal(Object):
    u"""A “deal” object constitutes a deal struck a priori between a buyer and a seller.

    A “deal” object constitutes a deal struck a priori between a buyer and a seller and indicates that
    this impression is available under the terms of that deal.
    """

    id = Field(String, required=True)
    bidfloor = Field(float)
    bidfloorcur = Field(String, 'USD')
    wseat = Field(Array(String))
    wadomain = Field(Array(String))
    at = Field(constants.AuctionType)
    ext = Field(Object)


class PMP(Object):
    u"""Top-level object for Direct Deals

    The “pmp” object contains a parent object for usage within the context of private marketplaces
    and the use of the RTB protocol to execute Direct Deals.
    """

    private_auction = Field(int)
    deals = Field(Array(Deal))
    ext = Field(Object)


class Impression(Object):
    u"""At least one impression object is required in a bid request object.

    The “imp” object desribes the ad position or impression being auctioned.
    A single bid request can include multiple “imp” objects,
    a use case for which might be an exchange that supports selling all ad positions on a given page as a bundle.
    Each “imp” object has a required ID so that bids can reference them individually.
    """

    id = Field(String, required=True)
    banner = Field(Banner)
    video = Field(Video)
    displaymanager = Field(String)
    displaymanagerver = Field(String)
    instl = Field(int)
    tagid = Field(String)
    bidfloor = Field(Decimal)
    bidfloorcur = Field(String, default='USD')
    secure = Field(int)
    iframebuster = Field(Array(String))
    pmp = Field(PMP)
    ext = Field(Object)


class Regulations(Object):
    u"""The “regs” object contains any legal, governmental, or industry regulations that apply to the request.

    The first regulation added signal whether or not the request falls under the United States
    Federal Trade Commission’s regulations for the United States Children’s Online Privacy
    Protection Act (“COPPA”). See the COPPA appendix for details.
    The regs object itself and all of its parameters are optional, so default values are not provided.
    If an optional parameter is not specified, it should be considered unknown.
    """

    coppa = Field(int)
    ext = Field(Object)


class BidRequest(Object):
    u"""Top-level bid request object.

    The top-level bid request object contains a globally unique bid request or auction ID.
    This “id” attribute is required as is at least one “imp” (i.e., impression) object.
    Other attributes are optional since an exchange may establish default values.
    """

    id = Field(String, required=True)
    imp = Field(Array(Impression), required=True)
    site = Field(Site)
    app = Field(App)
    device = Field(Device)
    user = Field(User)
    at = Field(constants.AuctionType, default=constants.AuctionType.SECOND_PRICE)
    tmax = Field(int)
    wseat = Field(Array(String))
    allimps = Field(int)
    cur = Field(Array(String))
    bcat = Field(Array(String))
    badv = Field(Array(String))
    regs = Field(Regulations)
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

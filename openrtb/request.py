from decimal import Decimal

from . import constants
from .base import Object, Array, Field


class Publisher(Object):
    id = Field(str)
    name = Field(str)
    cat = Field(Array(str))
    domain = Field(str)


class Producer(Object):
    id = Field(str)
    name = Field(str)
    cat = Field(Array(str))
    domain = Field(str)


class Geo(Object):
    lat = Field(float)
    lon = Field(float)
    country = Field(str)
    region = Field(str)
    regionfips104 = Field(str)
    metro = Field(str)
    city = Field(str)
    zip = Field(str)
    type = Field(constants.LocationType)

    def loc(self):
        if self.lat and self.lon:
            return self.lat, self.lon


class Segment(Object):
    id = Field(str)
    name = Field(str)
    value = Field(str)


class Data(Object):
    id = Field(str)
    name = Field(str)
    segment = Field(Array(Segment))


class User(Object):
    id = Field(str)
    buyerid = Field(str)
    yob = Field(int)
    gender = Field(str)
    keywords = Field(str)
    customdata = Field(str)
    geo = Field(Geo)
    data = Field(Array(Data))


class Device(Object):
    dnt = Field(int)
    ua = Field(str)
    ip = Field(str)
    geo = Field(Geo, default=Geo())
    didsha1 = Field(str)
    didmd5 = Field(str)
    dpidsha1 = Field(str)
    dpidmd5 = Field(str)
    ipv6 = Field(str)
    carrier = Field(str)
    language = Field(str)
    make = Field(str)
    model = Field(str)
    os = Field(str)
    osv = Field(str)
    js = Field(int)
    connectiontype = Field(constants.ConnectionType)
    devicetype = Field(constants.DeviceType)
    flashver = Field(str)

    def is_on_cellular(self):
        return self.connectiontype and self.connectiontype.is_cellular()


class Content(Object):
    id = Field(str)
    episode = Field(int)
    title = Field(str)
    series = Field(str)
    season = Field(str)
    url = Field(str)
    cat = Field(Array(str))
    videoquality = Field(constants.VideoQuality)
    keywords = Field(str)
    contentrating = Field(str)
    userrating = Field(str)
    context = Field(str)
    livestream = Field(int)
    sourcerelationship = Field(int)
    producer = Field(Producer)
    len = Field(int)


class Site(Object):
    id = Field(str)
    name = Field(str)
    domain = Field(str)
    cat = Field(Array(str))
    sectioncat = Field(Array(str))
    pagecat = Field(Array(str))
    page = Field(str)
    privacypolicy = Field(int)
    ref = Field(str)
    search = Field(str)
    publisher = Field(Publisher)
    content = Field(Content)
    keywords = Field(str)


class App(Object):
    id = Field(str)
    name = Field(str)
    domain = Field(str)
    cat = Field(Array(str))
    sectioncat = Field(Array(str))
    pagecat = Field(Array(str))
    ver = Field(str)
    bundle = Field(str)
    privacypolicy = Field(int)
    paid = Field(int)
    publisher = Field(Publisher)
    content = Field(Content)
    keywords = Field(str)


class Banner(Object):
    w = Field(int)
    h = Field(int)
    id = Field(str)
    pos = Field(constants.AdPosition)
    btype = Field(Array(constants.BannerType))
    battr = Field(Array(constants.CreativeAttribute))
    mimes = Field(Array(str))
    topframe = Field(int)
    expdir = Field(Array(constants.ExpandableDirection))
    api = Field(Array(constants.APIFramework))

    def blocked_types(self):
        return set(self.btype or [])

    def size(self):
        if self.w and self.h:
            return self.w, self.h


class Video(Object):
    mimes = Field(Array(str), required=True)
    linearity = Field(constants.VideoLinearity, required=True)
    minduration = Field(int, required=True)
    maxduration = Field(int, required=True)
    protocol = Field(constants.VideoProtocol, required=True)
    w = Field(int)
    h = Field(int)
    startdelay = Field(int)
    sequence = Field(int, 1)
    battr = Field(Array(constants.CreativeAttribute))
    maxextended = Field(int)
    minbitrate = Field(int)
    maxbitrate = Field(int)
    boxingallowed = Field(int)
    playbackmethod = Field(Array(constants.VideoPlaybackMethod))
    delivery = Field(Array(constants.ContentDeliveryMethod))
    pos = Field(constants.AdPosition)
    companionad = Field(Array(Banner))
    api = Field(Array(constants.APIFramework))


class Impression(Object):
    id = Field(str, required=True)
    banner = Field(Banner)
    video = Field(Video)
    displaymanager = Field(str)
    instl = Field(int)
    tagid = Field(str)
    bidfloor = Field(Decimal)
    bidfloorcur = Field(str, default='USD')
    iframebuster = Field(Array(str))
    ext = Field(Object)


class BidRequest(Object):
    id = Field(str, required=True)
    imp = Field(Array(Impression), required=True)
    site = Field(Site, default=Site())
    app = Field(App, default=App())
    device = Field(Device, default=Device())
    user = Field(User, default=User())
    at = Field(constants.AuctionType, default=constants.AuctionType.SECOND_PRICE)
    tmax = Field(int)
    wseat = Field(Array(str))
    allimpd = Field(int)
    cur = Field(Array(str))
    bcat = Field(Array(str))
    badv = Field(Array(str))
    ext = Field(Object)

    @staticmethod
    def minimal(id, imp_id):
        return BidRequest(id=id, imp=[Impression(id=imp_id, banner=Banner())])

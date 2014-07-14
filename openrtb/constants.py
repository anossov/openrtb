from . import base


class AuctionType(base.Enum):
    FIRST_PRICE = 1
    SECOND_PRICE = 2


class BannerType(base.Enum):
    TEXT = 1
    BANNER = 2
    JS = 3
    IFRAME = 4


class CreativeAttribute(base.Enum):
    AUDIO_AUTOPLAY = 1
    AUDIO_USER = 2
    EXPAND_AUTO = 3
    EXPAND_CLICK = 4
    EXPAND_ROLLOVER = 5
    VIDEO_AUTOPLAY = 6
    VIDEO_USER = 7
    POP = 8
    PROVOCATIVE = 9
    FLASHING = 10
    SURVEY = 11
    TEXT = 12
    INTERACTIVE = 13
    DIALOG = 14
    AUDIO_ONOFF = 15
    SKIPPABLE = 16


class AdPosition(base.Enum):
    UNKNOWN = 0
    VISIBLE = 1
    MAYBE_VISIBLE = 2
    OFFSCREEN = 3
    HEADER = 4
    FOOTER = 5
    SIDEBAR = 6
    FULLSCREEN = 7


class ConnectionType(base.Enum):
    UNKNOWN = 0
    ETHERNET = 1
    WIFI = 2
    CELLULAR_UNKNOWN_G = 3
    CELLULAR_2G = 4
    CELLULAR_3G = 5
    CELLULAR_4G = 6

    def is_cellular(self):
        return self.value > 3


class ExpandableDirection(base.Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    FULLSCREEN = 5


class ContentContext(base.Enum):
    VIDEO = 1
    GAME = 2
    MUSIC = 3
    APP = 4
    TEXT = 5
    OTHER = 6
    UNKNOWN = 7


class ContentDeliveryMethod(base.Enum):
    STREAMING = 1
    PROGRESSIVE = 2


class LocationType(base.Enum):
    GPS = 1
    IP = 2
    USER = 3


class DeviceType(base.Enum):
    MOBILE = 1
    PC = 2
    TV = 3
    PHONE = 4
    TABLET = 5
    CONNECTED_DEVICE = 6
    SET_TOP_BOX = 7


class APIFramework(base.Enum):
    VPAID1 = 1
    VPAID2 = 2
    MRAID = 3
    ORMMA = 4
    MRAID2 = 5


class VideoLinearity(base.Enum):
    LINEAR = 1
    NON_LINEAR = 2


class VideoProtocol(base.Enum):
    VAST1 = 1
    VAST2 = 2
    VAST3 = 3
    VAST1_WRAPPER = 4
    VAST2_WRAPPER = 5
    VAST3_WRAPPER = 6


class VideoPlaybackMethod(base.Enum):
    AUTOPLAY_SOUND_ON = 1
    AUTOPLAY_SOUND_OFF = 2
    CLICK_TO_PLAY = 3
    MOUSE_OVER = 4


class VideoQuality(base.Enum):
    UNKNOWN = 0
    PROFESSIONALLY_PRODUCED = 1
    PROSUMER = 2
    USER_GENERATED = 3


class CompanionType(base.Enum):
    STATIC = 1
    HTML = 2
    IFRAME = 3


class QAGMediaRating(base.Enum):
    ALL_AUDIENCES = 1
    OVER_12 = 2
    MATURE = 3


class NoBidReason(base.Enum):
    UNKNOWN = 0
    TECHNICAL_ERROR = 1
    INVALID_REQUEST = 2
    KNOWN_WEB_SPIDER = 3
    SUSPECTED_NON_HUMAN = 4
    CLOUD_OR_PROXY_IP = 5
    UNSUPPORTED_DEVICE = 6
    BLOCKED_PUBLISHER_OR_SITE = 7
    UNMATCHED_USER = 8
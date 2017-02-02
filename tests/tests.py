# -*- coding: utf-8 -*-

import unittest

import openrtb
import openrtb.base

BRQ = {
    'id': u'testbrqid',
    'tmax': 100,
    'at': 2,
    'app': {
        'id': u'appid',
        'name': u'appname',
        'cat': [u'IAB1', u'IAB2-2'],
        'publisher': {
            'id': u'pubid',
            'cat': [u'IAB3']
        },
        'content': {
            'id': u'contentid',
            'episode': 1,
            'producer': {
                'id': u'pubid',
                'cat': [u'IAB3']
            }
        },
        'keywords': u'key,word'
    },
    'device': {
        'ip': u'123.1.2.3',
        'make': u'Apple',
        'devicetype': 1,
        'geo': {
            'lat': 54.3123,
            'lon': 32.12312,
            'country': u'US'
        }
    },
    'user': {
        'id': u'userid',
        'yob': 2012,
        'data': [
            {
                'id': u'dataid',
                'segment': [{
                                'id': u'segmentid',
                                'name': u'yob',
                                'value': u'2012',
                                }]
            }
        ]
    },
    'imp': [
        {
            'id': u'testimpid',
            'bidfloorcur': u'USD',
            'banner': {
                'w': 320,
                'h': 50,
                'pos': 1,
                'mimes': [u'mime/type']
            }
        }
    ],
    'ext': {}
}


class TestFields(unittest.TestCase):
    def test_passthrough(self):
        self.assertEqual(openrtb.base.Field(int).deserialize(1), 1)

    def test_convert(self):
        self.assertEqual(openrtb.base.Field(int).deserialize('1'), 1)

    def test_convert_fail(self):
        with self.assertRaises(openrtb.base.ValidationError):
            openrtb.base.Field(int).deserialize('asd')

    def test_convert_enum_fail(self):
        with self.assertRaises(openrtb.base.ValidationError):
            openrtb.base.Field(openrtb.base.Enum).deserialize('asd')

    def test_convert_enum(self):
        self.assertEqual(openrtb.base.Field(openrtb.base.Enum).deserialize('1'), 1)

    def test_deserialize(self):
        class O(object):
            v = None
            @staticmethod
            def deserialize(v):
                O.v = v
                return 'test'

        self.assertEqual(openrtb.base.Field(O).deserialize('1'), 'test')
        self.assertEqual(O.v, '1')

    def test_unicode(self):
        self.assertEqual(openrtb.base.String(u'uni'), u'uni')

    def test_ascii(self):
        self.assertEqual(openrtb.base.String('uni'), u'uni')

    def test_utf8(self):
        self.assertEqual(openrtb.base.String('утф'), u'утф')

    def test_bad_utf8(self):
        self.assertEqual(openrtb.base.String('x\xff'), u'x')

    def test_convert_to_unicode(self):
        self.assertEqual(openrtb.base.String(1), u'1')

    def test_default_array(self):
        self.assertEqual(openrtb.base.Array(int)(None), [])

    def test_enum_int(self):
        self.assertEqual(openrtb.base.Enum(1), 1)

    def test_enum_convert_to_int(self):
        self.assertEqual(openrtb.base.Enum('1'), 1)

    def test_enum_convert_to_int_fail(self):
        with self.assertRaises(ValueError):
            openrtb.base.Enum('x')


class TestObjects(unittest.TestCase):
    def test_required(self):
        with self.assertRaises(openrtb.base.ValidationError):
            openrtb.request.BidRequest()

    def test_extra(self):
        s = openrtb.request.Site(extra='extra')
        self.assertEqual(s.extra, 'extra')

    def test_ds_extra(self):
        s = openrtb.request.Site.deserialize({'extra': 'extra'})
        self.assertEqual(s.extra, 'extra')

    def test_missing(self):
        s = openrtb.request.Site()
        self.assertEqual(s.extra, None)

    def test_ds_none(self):
        s = openrtb.request.Site.deserialize({'id': None})
        self.assertEqual(s.id, None)

    def test_bid_request_serialize_cycle(self):
        self.maxDiff = None
        brq = openrtb.request.BidRequest.deserialize(BRQ)
        self.assertDictEqual(BRQ, brq.serialize())


class TestGetters(unittest.TestCase):
    def test_brq_user(self):
        brq = openrtb.request.BidRequest.minimal('i', 'i')
        self.assertEqual(brq.get_user().__class__,
                         openrtb.request.User)
        brq.user = openrtb.request.User(id='t')
        self.assertEqual(brq.get_user().id, 't')

    def test_brq_app(self):
        brq = openrtb.request.BidRequest.minimal('i', 'i')
        self.assertEqual(brq.get_app().__class__,
                         openrtb.request.App)
        brq.app = openrtb.request.App(id='t')
        self.assertEqual(brq.get_app().id, 't')

    def test_brq_site(self):
        brq = openrtb.request.BidRequest.minimal('i', 'i')
        self.assertEqual(brq.get_site().__class__,
                         openrtb.request.Site)
        brq.site = openrtb.request.Site(id='t')
        self.assertEqual(brq.get_site().id, 't')

    def test_brq_device(self):
        brq = openrtb.request.BidRequest.minimal('i', 'i')
        self.assertEqual(brq.get_device().__class__,
                         openrtb.request.Device)
        brq.device = openrtb.request.Device(id='t')
        self.assertEqual(brq.get_device().id, 't')

    def test_banner_btypes(self):
        self.assertEqual(openrtb.request.Banner().blocked_types(), set())
        self.assertEqual(openrtb.request.Banner(btype=[openrtb.constants.BannerType.BANNER]).blocked_types(),
                         {openrtb.constants.BannerType.BANNER})

    def test_banner_size(self):
        self.assertEqual(openrtb.request.Banner().size(), None)
        self.assertEqual(openrtb.request.Banner(w=1, h=2).size(), (1, 2))

    def test_device_geo(self):
        self.assertEqual(openrtb.request.Device().get_geo().__class__,
                         openrtb.request.Geo)
        geo = openrtb.request.Geo()
        self.assertEqual(openrtb.request.Device(geo=geo).get_geo(), geo)

    def test_device_oncellular(self):
        self.assertFalse(openrtb.request.Device().is_on_cellular())
        self.assertTrue(openrtb.request.Device(connectiontype=openrtb.constants.ConnectionType.CELLULAR_2G).is_on_cellular())
        self.assertFalse(openrtb.request.Device(connectiontype=openrtb.constants.ConnectionType.WIFI).is_on_cellular())

    def test_geo_loc(self):
        self.assertEqual(openrtb.request.Geo().loc(), None)
        self.assertEqual(openrtb.request.Geo(lat=1, lon=2).loc(), (1, 2))


class TestMobileAdapter(unittest.TestCase):
    def test_adapter(self):
        mbrq = openrtb.mobile.BidRequest(
            id='mbrqid',
            imp=[
                openrtb.mobile.Impression(
                    impid='impid',
                    w=320,
                    h=50,
                    btype=[openrtb.constants.BannerType.BANNER],
                    battr=[openrtb.constants.CreativeAttribute.AUDIO_AUTOPLAY],
                    pos=openrtb.constants.AdPosition.OFFSCREEN
                )
            ],
            device=openrtb.mobile.Device(
                loc='1.23,4.56',
                country='US',
                make='Apple'
            ),
            site=openrtb.mobile.Site(
                sid='siteid',
                pub='sitepub',
                pid='sitepubid'
            ),
            app=openrtb.mobile.App(
                aid='appid',
                pub='apppub',
                pid='apppubid',
            ),
            user=openrtb.mobile.User(
                country='RU',
                zip='123456',
                uid='userid',
            ),
            restrictions=openrtb.mobile.Restrictions(
                bcat=['cat'],
                badv=['adv'],
            )
        )

        a = openrtb.mobile.OpenRTB20Adapter(mbrq)

        self.assertEqual(a.id, 'mbrqid')
        self.assertEqual(a.imp[0].banner.w, 320)
        self.assertEqual(a.imp[0].banner.h, 50)
        self.assertEqual(a.imp[0].banner.btype, [openrtb.constants.BannerType.BANNER])
        self.assertEqual(a.imp[0].banner.pos, openrtb.constants.AdPosition.OFFSCREEN)
        self.assertEqual(a.device.geo.country, 'US')
        self.assertEqual(a.device.geo.lat, 1.23)
        self.assertEqual(a.device.geo.lon, 4.56)
        self.assertEqual(a.site.publisher.id, 'sitepubid')
        self.assertEqual(a.site.publisher.name, 'sitepub')
        self.assertEqual(a.site.id, 'siteid')
        self.assertEqual(a.app.id, 'appid')
        self.assertEqual(a.user.geo.country, 'RU')
        self.assertEqual(a.user.geo.zip, '123456')
        self.assertEqual(a.user.id, 'userid')
        self.assertEqual(a.bcat, ['cat'])
        self.assertEqual(a.badv, ['adv'])

        self.assertEqual(a.brq.serialize(),
                         openrtb.mobile.OpenRTB20Adapter.deserialize(mbrq.serialize()).brq.serialize())


class TestConstants(unittest.TestCase):
    def test_init(self):
        self.assertEqual(openrtb.constants.AdPosition(2).name, 'MAYBE_VISIBLE')

    def test_clone(self):
        self.assertEqual(openrtb.constants.AdPosition(openrtb.constants.AdPosition.OFFSCREEN).name, 'OFFSCREEN')

    def test_int(self):
        self.assertEqual(int(openrtb.constants.ConnectionType(2)), 2)

    def test_str(self):
        self.assertEqual(str(openrtb.constants.AdPosition(2)), 'MAYBE_VISIBLE')

    def test_hash(self):
        self.assertEqual({openrtb.constants.AdPosition.OFFSCREEN: 'test'}[3], 'test')

    def test_unknown_str(self):
        self.assertIn('Unknown', str(openrtb.constants.BannerType(123)))

    def test_none_equal(self):
        self.assertFalse(None == openrtb.constants.BannerType.JS)

    def test_int_equal(self):
        self.assertEqual(openrtb.constants.BannerType.JS, 3)

    def test_constant_equal(self):
        self.assertEqual(openrtb.constants.BannerType.JS, openrtb.constants.BannerType(3))

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            openrtb.constants.BannerType.JS == openrtb.constants.CreativeAttribute.EXPAND_AUTO


class TestIAB(unittest.TestCase):
    def test_tier1(self):
        self.assertEqual(openrtb.iab.from_string('IAB1'), 'Arts & Entertainment')
        self.assertEqual(openrtb.iab.from_string('IAB18'), 'Style & Fashion')

    def test_tier2(self):
        self.assertEqual(openrtb.iab.from_string('IAB17-33'), 'Sports: Scuba Diving')

    def test_noprefix(self):
        self.assertEqual(openrtb.iab.from_string('7-32'), 'Health & Fitness: Nutrition')

    def test_bad(self):
        self.assertEqual(openrtb.iab.from_string('IAB99-99'), 'IAB99-99')


class TestMacros(unittest.TestCase):
    TPL = ('${AUCTION_ID}/${AUCTION_BID_ID}/${AUCTION_IMP_ID}/'
           '${AUCTION_SEAT_ID}/${AUCTION_AD_ID}/${AUCTION_PRICE}/${AUCTION_CURRENCY}')

    def test_sub(self):
        brq = openrtb.request.BidRequest.minimal('reqid', 'impid')
        brp = openrtb.response.BidResponse(
            id='wharrgarbl',
            seatbid=[openrtb.response.SeatBid(
                seat='seatid',
                bid=[openrtb.response.Bid(
                    id='bidid',
                    impid='impid',
                    adid='adid',
                    price=0
                )]
            )],
            bidid='bidid'
        )
        self.assertEqual(openrtb.macros.substitution(brq, brp, 0.1, self.TPL),
                         'reqid/bidid/impid/seatid/adid/0.1/USD')

    def test_nonmacro(self):
        self.assertEqual(openrtb.macros.substitution(
            openrtb.request.BidRequest.minimal('r', 'i'),
            openrtb.response.BidResponse.minimal('id', 'bidid', 'impid', 0.1),
            0.2,
            '${AUCTION_TEST}'
        ), '${AUCTION_TEST}')

    def test_empty(self):
        self.assertEqual(openrtb.macros.substitution(
            openrtb.request.BidRequest.minimal('rid', 'rimpid'),
            openrtb.response.BidResponse.minimal('respid', 'bidid', 'impid', 0.1),
            0.2,
            self.TPL
        ), 'rid//impid///0.2/USD')

if __name__ == '__main__':
    unittest.main()
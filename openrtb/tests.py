import unittest

import openrtb


class TestDeSerialize(unittest.TestCase):
    def test_bid_request_sanity(self):
        self.maxDiff = None
        data = {
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
                'ip': u'123.1.2.3.',
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
        brq = openrtb.request.BidRequest.deserialize(data)
        self.assertDictEqual(data, brq.serialize())


if __name__ == '__main__':
    unittest.main()
import os
import uuid
from unittest import TestCase
from unittest.mock import patch


class MGAClientTestCase(TestCase):

    def test_make_parameters(self):
        from mgaclient import MGAClient
        from mgaclient.consts import DATATYPE_EPHEMERIS, DATATYPE_ALMANAC, DATATYPE_AUX, DATATYPE_POS
        from mgaclient.consts import FORMAT_MGA, FORMAT_AID
        from mgaclient.consts import GNSS_GPS, GNSS_QZSS, GNSS_BEIDOU, GNSS_GALILEO, GNSS_GLONASS

        class Item:
            def __init__(self, token, datatype, dataformat, gnss, result):
                self.token = token
                self.datatype = datatype
                self.dataformat = dataformat
                self.gnss = gnss

                self.result = result

        items = [
            Item('tokenA', [DATATYPE_EPHEMERIS], FORMAT_AID, [GNSS_GPS], {
                'token': 'tokenA',
                'datatype': 'eph',
                'format': 'aid',
                'gnss': 'gps',
            }),
            Item('tokenB', [DATATYPE_EPHEMERIS, DATATYPE_ALMANAC], FORMAT_MGA, [GNSS_GPS, GNSS_QZSS], {
                'token': 'tokenB',
                'datatype': 'eph,alm',
                'format': 'mga',
                'gnss': 'gps,qzss',
            }),
            Item('tokenC', [DATATYPE_EPHEMERIS, DATATYPE_ALMANAC, DATATYPE_AUX], FORMAT_MGA,
                 [GNSS_GPS, GNSS_QZSS, GNSS_GLONASS], {
                     'token': 'tokenC',
                     'datatype': 'eph,alm,aux',
                     'format': 'mga',
                     'gnss': 'gps,qzss,glo',
                 }),
            Item('tokenD', [DATATYPE_POS], FORMAT_MGA, [GNSS_BEIDOU, GNSS_GALILEO], {
                'token': 'tokenD',
                'datatype': 'pos',
                'format': 'mga',
                'gnss': 'bds,gal',
            }),
        ]

        for item in items:
            client = MGAClient(item.token, item.datatype, item.dataformat, item.gnss)
            self.assertDictEqual(item.result, client.make_parameters())

    def test_get(self):
        with patch('requests.get', return_value=None) as p:
            from mgaclient import MGAClient

            client = MGAClient('token', timeout=0)
            client.get()
            self.assertEqual('https://online-live1.services.u-blox.com/GetOnlineData.ashx?token=token&datatype=eph,alm,aux&format=mga&gnss=gps,qzss', p.call_args[0][0])

    def test_save(self):
        test_filename = '%s.bin' % uuid.uuid4()

        try:
            from requests import Response

            response = Response
            response.status_code = 200
            response.raw = b'mga binary code'

            with patch('requests.get', return_value=response):
                from mgaclient import MGAClient

                client = MGAClient('token', timeout=0)
                client.save(test_filename)
                self.assertTrue(os.path.exists(test_filename))

                with open(test_filename, 'br') as f:
                    self.assertEqual(b'mga binary code', f.read())
        finally:
            if os.path.exists(test_filename):
                os.unlink(test_filename)

from typing import Tuple
from urllib.parse import urlencode

import requests
from requests import Response

from mgaclient.consts import DATATYPE_EPHEMERIS, DATATYPE_ALMANAC, DATATYPE_AUX, FORMAT_MGA, GNSS_GPS, GNSS_QZSS


class MGAClient(object):
    _endpoints = [
        'https://online-live1.services.u-blox.com/GetOnlineData.ashx',
        'https://online-live2.services.u-blox.com/GetOnlineData.ashx',
        'https://online-live3.services.u-blox.com/GetOnlineData.ashx',
    ]

    def __init__(self, token: str, datatype: Tuple[str] = (DATATYPE_EPHEMERIS, DATATYPE_ALMANAC, DATATYPE_AUX),
                 dataformat: str = FORMAT_MGA, gnss: Tuple[str] = (GNSS_GPS, GNSS_QZSS), timeout: int = 5):
        self.token = token
        self.datatype = ','.join(datatype)
        self.format = dataformat
        self.gnss = ','.join(gnss)

        self.timeout = timeout

    def make_parameters(self) -> dict:
        return {
            'token': self.token,
            'datatype': self.datatype,
            'format': self.format,
            'gnss': self.gnss,
        }

    def get(self) -> Response:
        for endpoint in self._endpoints:
            return requests.get('%s?%s' % (endpoint, urlencode(self.make_parameters(), safe=',')),
                                timeout=self.timeout)

    def save(self, filename: str) -> bool:
        response = self.get()
        f = None
        try:
            f = open(filename, 'wb')
            f.write(response.raw)
        finally:
            if f:
                f.close()
        return True

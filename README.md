# pymgaclient
[![codecov](https://codecov.io/gh/key/pymgaclient/branch/master/graph/badge.svg)](https://codecov.io/gh/key/pymgaclient)

Python utilities for u-blox MultiGNSS Assitance Services


# Usage

```python
from mgaclient import MGAClient

client = MGAClient('SET-YOUR-TOKEN-HERE', )
client.save('mga.bin')
```


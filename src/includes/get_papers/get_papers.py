import sys
import urllib.request
from urllib.error import HTTPError

BASE_URL = 'http://dx.doi.org/'

doi = '10.3390/e23081064'
dois = ['10.1016/j.artint.2021.103457','10.1109/MIS.2019.2957223','10.3390/e23081064']


url = BASE_URL + doi
req = urllib.request.Request(url)
req.add_header('Accept', 'application/x-bibtex')
try:
    with urllib.request.urlopen(req) as f:
        bibtex = f.read().decode()
    print(bibtex)
except HTTPError as e:
    if e.code == 404:
        print('DOI not found.')
    else:
        print('Service unavailable.')
    sys.exit(1)

print(type(bibtex))
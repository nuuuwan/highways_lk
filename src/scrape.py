
from bs4 import BeautifulSoup
from utils import tsv, www

from __constants import RAW_HTML_FILE, ROADS_FILE, URL_RAW


def download_raw():
    www.download_binary(URL_RAW, RAW_HTML_FILE)


def parse_raw():

    with open(RAW_HTML_FILE, 'rb') as fin:
        html = fin.read()
        fin.close()

    soup = BeautifulSoup(html, 'html.parser')
    roads_index = {}
    for table in soup.find_all('table'):
        for tr in table.find_all('tr'):
            td_text_list = list(
                map(
                    lambda td: td.text,
                    tr.find_all('td'),
                )
            )
            if len(td_text_list) != 3:
                continue
            if td_text_list[0] == '':
                continue
            road_id, desc, length_str = td_text_list
            length = (float)(length_str)
            roads_index[road_id] = dict(
                road_id=road_id,
                desc=desc,
                length=length,
            )

    roads = sorted(
        list(roads_index.values()),
        key=lambda d: d['road_id'],
    )
    tsv.write(ROADS_FILE, roads)


if __name__ == '__main__':
    download_raw()
    parse_raw()

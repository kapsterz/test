import urllib
import datetime
import os
import re

def download(ident):
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/" \
          "get_provinceData.php?country=UKR&provinceID=%02d&year1=1981&year2=2018&type=Mean" % ident
    print(url)
    vhi_url = urllib.urlopen(url)
    now = datetime.datetime.now().strftime("%Y_%m_%d-%Hh")
    out = open('vhi_id_%02d.csv' % ident, 'wb')
    out.write(re
              .sub(r'(?is)Mean data for UKR.*<br><tt><pre>', '', vhi_url.read())
              .replace('</pre></tt>', '')
              .replace(',,', ',')
              .replace(', ', ',')
              .replace('  ', ',,')
              .replace(', ', ',')
              .replace(' ', ','))
    out.close()
    os.rename('vhi_id_%02d.csv' % ident, now + '_vhi_id_%02d.csv' % ident)
    print ("VHI is downloaded...")


for ident in range(1, 28):
    download(ident)

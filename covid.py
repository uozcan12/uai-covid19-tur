import bs4
import requests
from bs4 import BeautifulSoup as bs
import urllib.request
import re
import datetime
import pandas as pd
from git import Repo

url='https://covid19.saglik.gov.tr/'
soup=bs(urllib.request.urlopen(url), "html5lib")
#print(soup)

def month_string_to_number(string):
    m = {
        'OCAK': "01",
        'ŞUBAY': "02",
        'MART': "03",
        'NİSAN':"04",
         'MAYIS':"05",
         'HAZİRAN':"06",
         'TEMMUZ':"07",
         'AĞUSTOS':8,
         'EYLÜL':9,
         'EKİM':10,
         'KASIM':11,
         'ARALIK':12
        }
    s = string.strip()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

a=month_string_to_number(soup.find('p',class_='p2').text)
tarih=soup.find('p',class_='p1').text + "." + str(a) + "." +soup.find('p',class_='p3').text
gunluk_vaka_sayisi = soup.findAll('span')[15].text.replace(".","")
toplam_vaka_sayisi=soup.findAll('span')[3].text.replace(".","")
gunluk_iyilesen_sayisi = soup.findAll('span')[19].text.replace(".","")
toplam_iyilesen_sayisi = soup.findAll('span')[11].text.replace(".","")
gunluk_vefat_sayisi = soup.findAll('span')[17].text.replace(".","")
toplam_vefat_sayisi = soup.findAll('span')[5].text.replace(".","")
gunluk_test_sayisi=soup.findAll('span')[13].text.replace(".","")
toplam_test_sayisi = soup.findAll('span')[1].text.strip().replace(".","")

df = pd.read_csv('./data/COVID.csv', index_col=False)
indexes=df[df.columns[9]].tolist()


'''print("Tarih " + soup.find('p',class_='p1').text + "." + str(a) + "." +soup.find('p',class_='p3').text)
print("Toplam Test Sayısı " + soup.findAll('span')[1].text.strip())
print("Toplam Vaka Sayısı " + soup.findAll('span')[3].text)
print("Toplam Vefat Sayısı " + soup.findAll('span')[5].text)
print("Toplam Yoğun Bakım Hasta Sayısı " + soup.findAll('span')[7].text)
print("Toplam Entübe Hasta Sayısı " + soup.findAll('span')[9].text)
print("Toplam İyileşen Hasta Sayısı " + soup.findAll('span')[11].text)
print("Bugünkü Test Sayısı " + soup.findAll('span')[13].text)
print("Bugünkü Vaka Sayısı " + soup.findAll('span')[15].text)
print("Bugünkü Vefat Sayısı " + soup.findAll('span')[17].text)
print("Bugünkü İyileşen Sayısı " + soup.findAll('span')[19].text)
'''
with open('data/COVID.csv','a') as fd:
    fd.write(tarih+","+gunluk_vaka_sayisi+","+toplam_vaka_sayisi+","+gunluk_iyilesen_sayisi+","+toplam_iyilesen_sayisi+","+gunluk_vefat_sayisi
    +","+toplam_vefat_sayisi+","+gunluk_test_sayisi+","+toplam_test_sayisi+","+str(indexes[-1]+1)+"\n")
    fd.close()

#repo_dir = 'uai-covid19-tur'
#repo = Repo(repo_dir)
repo = Repo()
file_list = [
    'Pipfile',
    'Pipfile.lock',
    'requirements.txt',
    'covid.py',
    'data/COVID.csv'
]
commit_message = 'added git for python library & test git push'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()

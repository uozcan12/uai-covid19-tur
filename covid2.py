from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path='chromedriver/chromedriver')
driver.get("https://covid19.saglik.gov.tr/?lang=tr-TR")
print ("Headless Chrome Initialized")

def month_string_to_number(string):
    m = {
        'OCAK': "01",
        'ŞUBAY': "02",
        'MART': "03",
        'NİSAN':"04",
         'MAYIS':"05",
         'HAZİRAN':"06",
         'TEMMUZ':"07",
         'AĞUSTOS':"08",
         'EYLÜL':"09",
         'EKİM':"10",
         'KASIM':"11",
         'ARALIK':"12"
        }
    s = string.strip()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

a=month_string_to_number(driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div/p[2]").text)
tarih=driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div/p[1]").text + "." + str(a) + "." + driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div/p[3]").text
gunluk_vaka_sayisi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div/ul/li[2]/span[2]").text.replace(".","")
toplam_vaka_sayisi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/ul/li[2]/span[2]").text.replace(".","")
gunluk_iyilesen_sayisi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div/ul/li[4]/span[2]").text.replace(".","")
toplam_iyilesen_sayisi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/ul/li[6]/span[2]").text.replace(".","")
gunluk_vefat_sayisi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div/ul/li[3]/span[2]").text.replace(".","")
toplam_vefat_sayisi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/ul/li[3]/span[2]").text.replace(".","")
gunluk_test_sayisi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div/ul/li[1]/span[2]").text.replace(".","")
toplam_test_sayisi = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/ul/li[1]/span[2]").text.strip().replace(".","")

df = pd.read_csv('./data/COVID.csv', index_col=False)
indexes=df[df.columns[9]].tolist()

with open('data/COVID.csv','a') as fd:
    fd.write(tarih+","+gunluk_vaka_sayisi+","+toplam_vaka_sayisi+","+gunluk_iyilesen_sayisi+","+toplam_iyilesen_sayisi+","+gunluk_vefat_sayisi
    +","+toplam_vefat_sayisi+","+gunluk_test_sayisi+","+toplam_test_sayisi+","+str(indexes[-1]+1)+"\n")
    fd.close()
driver.quit()

import time
import openpyxl
from selenium import webdriver
from openpyxl import load_workbook
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import utils

def parse_page(range_start,range_stop,driver,df):
    for sonuc in range(range_start, range_stop):
        driver.switch_to_window(driver.window_handles[0])
        time.sleep(0.3)
        driver._switch_to.active_element
        time.sleep(0.3)

        # gather result texts
        yil2 = driver.find_element_by_css_selector(
            ".watable > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(3)" % sonuc).text
        baslik = driver.find_element_by_css_selector(
            ".watable > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(4)" % sonuc).text
        tur = driver.find_element_by_css_selector(
            ".watable > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(5)" % sonuc).text
        sonuclar = driver.find_element_by_css_selector(
            ".watable > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(1) > span:nth-child(1)" % sonuc).click()
        time.sleep(0.5)
        sonuc_ust_baslik = driver.find_element_by_css_selector("tr.renkp:nth-child(2) > td:nth-child(3)").text
        sonuc_alt_metin = driver.find_element_by_css_selector("#td0").text

        yaz = sonuc_ust_baslik.find("Yazar:")
        dan = sonuc_ust_baslik.find("Danışman:")
        yer = sonuc_ust_baslik.find("Yer Bilgisi:")
        kon = sonuc_ust_baslik.find("Konu:")
        diz = sonuc_ust_baslik.find("Dizin:")
        ana = sonuc_alt_metin.find("Kelimeler:")

        yazar = sonuc_ust_baslik[(yaz + 6): dan]
        danisman = sonuc_ust_baslik[(dan + 9): yer]
        yer_bilgisi = sonuc_ust_baslik[(yer + 12): kon]
        konu = sonuc_ust_baslik[(kon + 5): diz]
        dizin = sonuc_ust_baslik[(diz + 6):]

        if ana != -1:
            anahtar = sonuc_alt_metin[(ana + 10):]
        else:
            anahtar = " "

        # arrange results for writing
        final = [baslik, yil2, tur, yazar, danisman, yer_bilgisi, konu, dizin, anahtar]
        df.index += 1
        df.loc[0] = final
        # write and out
        # (bu blokta try isimde buyuk yumusak g varsa hata verdigi icin var)
        """
        try:
            #sheet.append(final)
        except:
            print('pass, exception')
            result_df
        #workbook.save("new.xlsx")
        """
        time.sleep(0.05)

        # close detail view
        driver.find_element_by_css_selector(".ui-icon").click()
        try:
            # wait.until(EC.element_to_be_clickable(sonuclar))
            driver.find_element_by_css_selector(".ui-icon").click()
        except:
            pass

        time.sleep(0.05)
        # change back into main frame
        # //*[@id="dialog-modal"]driver.switch_to_window(driver.window_handles[0])

    # click next page
    driver.find_element_by_css_selector(".pagination > ul:nth-child(1) > li:nth-child(7) > a:nth-child(1)").click()
    return df

def main_scrap(yil):

    driver = webdriver.Chrome()
    main_url = "https://tez.yok.gov.tr/UlusalTezMerkezi/tarama.jsp"
    counter = 0

    """
    workbook = load_workbook(filename = "new.xlsx")
    sheet = workbook.active
    """

    wait = WebDriverWait(driver, 10)


    #ana dongu yılları cevirecek
    df = pd.DataFrame(
        columns=['baslik', 'yil', 'tur', 'yazar', 'danisman', 'yer bilgisi', 'konu', 'dizin', 'anahtar'])

    #arama sayfasına gir
    driver.get(main_url)
    main_page = driver.window_handles[0]

    #konu sec
    select_button = driver.find_element_by_xpath("/html/body/div[2]/div[1]/table/tbody/tr[2]/td/div/div[1]/form/table/tbody/tr/td/table/tbody/tr[6]/td[2]/input[2]").click()

    #sayfa gecisi (pop-up)
    konu = driver.window_handles[1]
    driver.switch_to_window(konu)
    time.sleep(1)

    #Konuya tikla (din 49, felsefe 65)
    my_konu = driver.find_element_by_css_selector("tr.renka:nth-child(65) > td:nth-child(1) > a:nth-child(1)").click()

    #geri don
    driver.switch_to_window(main_page)

    #yil sec
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/table/tbody/tr[2]/td/div/div[1]/form/table/tbody/tr/td/table/tbody/tr[2]/td[6]/select[1]/option[%d]" % yil).click()
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/table/tbody/tr[2]/td/div/div[1]/form/table/tbody/tr/td/table/tbody/tr[2]/td[6]/select[2]/option[%d]" % yil).click()

    #bul tuşuna bas
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/table/tbody/tr[2]/td/div/div[1]/form/table/tbody/tr/td/table/tbody/tr[8]/td/input[3]").click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="divuyari"]')))

    #sonuc sayisini al
    results_text = driver.find_element_by_xpath('//*[@id="divuyari"]').text
    x1 = results_text.split(' ')
    sonuc_sayisi = x1[2]
    print(sonuc_sayisi)
    sonuc_sayisi = int(sonuc_sayisi)

    #max 2000 sonuc gosteriliyor
    if sonuc_sayisi > 2000:
        sonuc_sayisi = 2000
        print("warning year" + str(yil))

    # sonuc sayisina gore kac sayfa oldugunu bul ve son sayfaya kac tane sonuc kaldigini cikar
    # sayfa sayisi +1'ler range fonksiyonu son degeri kapsamadigi icin var
    if sonuc_sayisi >= 30:

        if sonuc_sayisi % 30 == 0 :
            sayfa_sayisi = int(sonuc_sayisi / 30) + 1
            son_sayfa = sayfa_sayisi
            artan = sonuc_sayisi % 30

        else:
            sayfa_sayisi = int( sonuc_sayisi / 30 ) + 1
            artan = sonuc_sayisi % 30
            son_sayfa = sayfa_sayisi

    elif sonuc_sayisi <= 30 and sonuc_sayisi > 0 :
        sayfa_sayisi = 1
        artan = (sonuc_sayisi % 30)
        son_sayfa = 1

    else:
        sayfa_sayisi = "sonuc yok"
    print(sayfa_sayisi, son_sayfa, sonuc_sayisi, artan)

    #sonucların icerisinde gezinip gerekli bilgiyi cek, dosyaya yazdır
    #iteration over total pages
    for sayfa in range(1, sayfa_sayisi+1):
        print(sayfa)
        #checkpoint for if any result exists
        if sayfa_sayisi != "sonuc yok":

            #checkpoint for if the page is last  or contains 30 results
            if sayfa != son_sayfa:
                df = parse_page(1,31,driver,df)
                #iterartion over pages with 30 results

            elif sayfa == son_sayfa :
                #insert residual loop here
                df = parse_page(1,artan+1,driver,df)
        else:
            break
        counter += 1

    utils.save_var(df, 'result_dataframe'+str(yil))
    del df
    driver.close()

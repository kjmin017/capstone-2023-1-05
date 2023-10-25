# -*- coding: utf-8, euc-kr -*-
from ast import main
from imp import reload
import os
import profile
from re import T
from ssl import Options
import time
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pyautogui
import urllib.request

## Parameter variable
query = input()
i = 1

if __name__ == "__main__":
    # ����̹� ����
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": os.getcwd() }
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome()
    driver.minimize_window()
    

    # Ư��ǿ� �κ� �˻�����Ʈ�� �̵�
    driver.get('http://kportal.kipris.or.kr/kportal/search/total_search.do')
    driver.implicitly_wait(5)

    # Element ã�� �� send keyu
    driver.find_element(By.XPATH, '//*[@id="searchKeyword"]').send_keys(query+Keys.ENTER)
    time.sleep(1)

    # Ư��ǿ� �κи� Ŭ��
    driver.find_element(By.XPATH, '//*[@id="searchPatentBtn"]/button/span[1]').click()
    time.sleep(1)

    # �˻� ��� �� a�±� Ŭ�� �κ�
    driver.find_element(By.XPATH, '//*[@id="patentResultList"]/article[1]/div/div[1]/h1/a').click()
    
    
    # �˾�â���� focusing �̵�
    main_window_handle = None
    while not main_window_handle:
        main_window_handle = driver.current_window_handle
    
    popup_window_handle = None
    while not popup_window_handle:
        for handle in driver.window_handles:
            if handle != main_window_handle:
                popup_window_handle = handle
                break

    driver.switch_to.window(popup_window_handle)
    driver.minimize_window()
    
    while True:
        try:
            # ������������ �� Ŭ��
            driver.implicitly_wait(10)
            tab = driver.find_element(By.XPATH, '//*[@id="liView09"]/a')
            tab.click()
            driver.implicitly_wait(10)

            # ������ iframe���� �̵�
            iframe = driver.find_element(By.TAG_NAME, 'iframe')
            driver.switch_to.frame(iframe)

            # �������������� pdf�� ������ ���� ������ �Ѿ
            try:
                button = driver.find_element(By.XPATH, '/html/body/div/div/table/tbody/tr[1]/td[2]/a/img')
                button.click()
                # ���ο� popup���� switching
                captcha_window_handle = None
                while not captcha_window_handle:
                    for handle in driver.window_handles:
                        if handle != main_window_handle and handle != popup_window_handle:
                            captcha_window_handle = handle
                            break
                driver.switch_to.window(captcha_window_handle)
                driver.minimize_window()

                # ������ iframe���� �̵�
                iframe = driver.find_element(By.TAG_NAME, 'iframe')
                driver.switch_to.frame(iframe)
                bs4 = BeautifulSoup(driver.page_source, 'lxml') # pip install lxml
                img = bs4.find('img')

                # �̹�����ũ�� �����ͼ� captcha ���� ��������
    
                print("link:",'http://kpat.kipris.or.kr'+img['src'])
                driver.switch_to.default_content()
    
                time.sleep(5)
                bs4 = BeautifulSoup(driver.page_source, 'lxml')
                txt = str(bs4.find_all('script')[2].get_text())
    
                # �ʿ���� �������Ź� ����������ȣ ����
                src = txt.split('document.getElementById("pdfViewFrame").src = "')[1].split('";')[0]
                src =src.replace('amp;','')
    
                # captcha ��ȸ�ϴ� ��ũ��Ʈ jquery �̿�
                script ='$("#pdfViewFrame").show();\
                $("#bgBox").css("display","none");\
                $("#simpleCaptcha").css("display","none");\
                showPopLoadingBar();\
                document.getElementById("pdfViewFrame").src = "'+src+'";\
                resizeH();'
                driver.execute_script(script)
                driver.implicitly_wait(5)
    
                # �ٿ�ε� �ޱ�
                '''
                options = webdriver.ChromeOptions()
                options.add_experimental_option('prefs', {
                    "download.default_directory": "C:/Users", #Change default directory for downloads
                    "download.prompt_for_download": False, #To auto download the file
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
                })

                driver = webdriver.Chrome(options = options)
                driver.get(src)
                time.sleep(3)
                pyautogui.press('enter')
                ''' # 1��° ���

                response = urllib.request.urlopen(src)    
                file = open("%s%d.pdf" % (query, i), 'wb')
                file.write(response.read())
                file.close() # 2��° ���
                time.sleep(1)

                # PDF �ٿ�ް� ���� ������ �Ѿ��
                driver.switch_to.window(popup_window_handle)
                driver.minimize_window()
                element = driver.find_element(By.XPATH, '/html')
                if i%30 == 0:
                    element.send_keys(Keys.ARROW_RIGHT)
                else:
                    element.send_keys(Keys.ARROW_DOWN)
                i = i+1
                driver.implicitly_wait(5)

            except:
                element = driver.find_element(By.XPATH, '/html')
                if i%30 == 0:
                    element.send_keys(Keys.ARROW_RIGHT)
                else:
                    element.send_keys(Keys.ARROW_DOWN)
                i = i+1
                driver.implicitly_wait(5)
                driver.switch_to.window(popup_window_handle)
                driver.minimize_window()
        except:
            element = driver.find_element(By.XPATH, '/html')
            if i%30 == 0:
                element.send_keys(Keys.ARROW_RIGHT)
            else:
                element.send_keys(Keys.ARROW_DOWN)
                i = i+1
    
    time.sleep(10)
    driver.quit()
    
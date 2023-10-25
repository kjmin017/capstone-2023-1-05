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
    # 드라이버 설정
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": os.getcwd() }
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome()
    driver.minimize_window()
    

    # 특허실용 부분 검색사이트로 이동
    driver.get('http://kportal.kipris.or.kr/kportal/search/total_search.do')
    driver.implicitly_wait(5)

    # Element 찾은 후 send keyu
    driver.find_element(By.XPATH, '//*[@id="searchKeyword"]').send_keys(query+Keys.ENTER)
    time.sleep(1)

    # 특허실용 부분만 클릭
    driver.find_element(By.XPATH, '//*[@id="searchPatentBtn"]/button/span[1]').click()
    time.sleep(1)

    # 검색 결과 후 a태그 클릭 부분
    driver.find_element(By.XPATH, '//*[@id="patentResultList"]/article[1]/div/div[1]/h1/a').click()
    
    
    # 팝업창으로 focusing 이동
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
            # 통합행정정보 탭 클릭
            driver.implicitly_wait(10)
            tab = driver.find_element(By.XPATH, '//*[@id="liView09"]/a')
            tab.click()
            driver.implicitly_wait(10)

            # 프레임 iframe으로 이동
            iframe = driver.find_element(By.TAG_NAME, 'iframe')
            driver.switch_to.frame(iframe)

            # 통합행정정보에 pdf가 없으면 다음 탭으로 넘어감
            try:
                button = driver.find_element(By.XPATH, '/html/body/div/div/table/tbody/tr[1]/td[2]/a/img')
                button.click()
                # 새로운 popup으로 switching
                captcha_window_handle = None
                while not captcha_window_handle:
                    for handle in driver.window_handles:
                        if handle != main_window_handle and handle != popup_window_handle:
                            captcha_window_handle = handle
                            break
                driver.switch_to.window(captcha_window_handle)
                driver.minimize_window()

                # 프레임 iframe으로 이동
                iframe = driver.find_element(By.TAG_NAME, 'iframe')
                driver.switch_to.frame(iframe)
                bs4 = BeautifulSoup(driver.page_source, 'lxml') # pip install lxml
                img = bs4.find('img')

                # 이미지링크를 가져와서 captcha 문자 가져오기
    
                print("link:",'http://kpat.kipris.or.kr'+img['src'])
                driver.switch_to.default_content()
    
                time.sleep(5)
                bs4 = BeautifulSoup(driver.page_source, 'lxml')
                txt = str(bs4.find_all('script')[2].get_text())
    
                # 필요없는 문자제거및 문서고유번호 추출
                src = txt.split('document.getElementById("pdfViewFrame").src = "')[1].split('";')[0]
                src =src.replace('amp;','')
    
                # captcha 우회하는 스크립트 jquery 이용
                script ='$("#pdfViewFrame").show();\
                $("#bgBox").css("display","none");\
                $("#simpleCaptcha").css("display","none");\
                showPopLoadingBar();\
                document.getElementById("pdfViewFrame").src = "'+src+'";\
                resizeH();'
                driver.execute_script(script)
                driver.implicitly_wait(5)
    
                # 다운로드 받기
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
                ''' # 1번째 방법

                response = urllib.request.urlopen(src)    
                file = open("%s%d.pdf" % (query, i), 'wb')
                file.write(response.read())
                file.close() # 2번째 방법
                time.sleep(1)

                # PDF 다운받고 다음 페이지 넘어가기
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
    
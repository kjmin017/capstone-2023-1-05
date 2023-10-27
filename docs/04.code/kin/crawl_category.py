import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import pandas as pd
import os

# 저장할 파일명
filename = 'naver_kin_cate'
filecount = 1
# 검색 결과 페이지 수
pages = 99
count = 1

# 엑셀 파일 생성





dirid_list=[
            'https://kin.naver.com/qna/kinupList.naver?dirId=11&queryTime=2023-07-17%2016%3A37%3A00&page=',
            'https://kin.naver.com/qna/kinupList.naver?dirId=3&queryTime=2023-07-17%2016%3A53%3A46&page=',
            'https://kin.naver.com/qna/kinupList.naver?dirId=6&queryTime=2023-07-17%2016%3A53%3A59&page=',
            'https://kin.naver.com/qna/kinupList.naver?dirId=10&queryTime=2023-07-17%2016%3A54%3A09&page=',
            'https://kin.naver.com/qna/kinupList.naver?dirId=12&queryTime=2023-07-17%2016%3A54%3A22&page=',
            'https://kin.naver.com/qna/kinupList.naver?dirId=1&queryTime=2023-07-17%2016%3A51%3A16&page=',
            'https://kin.naver.com/qna/kinupList.naver?dirId=8&queryTime=2023-07-17%2016%3A51%3A56&page=',
            'https://kin.naver.com/qna/kinupList.naver?dirId=4&queryTime=2023-07-17%2016%3A54%3A40&page=',
            'https://kin.naver.com/qna/kinupList.naver?dirId=5&queryTime=2023-07-17%2016%3A54%3A56&page=',
            'https://kin.naver.com/qna/kinupList.naver?dirId=2&queryTime=2023-07-17%2016%3A55%3A15&page=',
            'https://kin.naver.com/qna/expertAnswerList.naver?dirId=7&queryTime=2023-07-17%2016%3A55%3A29&page='
            'https://kin.naver.com/qna/kinupList.naver?dirId=9&queryTime=2023-07-17%2016%3A56%3A06&page='
            ]
# 검색 페이지를 돌면서 크롤링 수행
#try:
for i in range(1, 12):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['제목', '질문', '답변'])
    data = pd.read_excel(f'naver_kin_cate_{i}.xlsx')
    
    for index, row in data.iterrows():
        title = row['제목']
        content = row['질문']
        answer = row['답변']
        print('추가됨', index)
        ws.append([title, content, answer])
    for page in range(1, pages + 1):
        url = dirid_list[i-1]+str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        questions = soup.select('div > table > tbody > tr > td.title > a')
        for question in questions:
            # 각 질문 페이지를 열어서 내용 크롤링
            question_url = 'https://kin.naver.com' + question['href']
            question_response = requests.get(question_url)
            question_soup = BeautifulSoup(question_response.content, 'html.parser')
            try:
                question_title = question_soup.select_one('.c-heading__title-inner').get_text(strip=True)
            except:
                continue
            try:
                question_content = question_soup.select_one('.c-heading__content').get_text(strip=True)
            except:
                question_content = question_title

            # 답변도 크롤링
            answer_content = ''
            answer = question_soup.select_one('.se-viewer')
            try:
                answer_content = answer.get_text('\n', strip=True)
            except:
                continue
            if answer_content == "":
                answer = question_soup.select_one('.c-heading-answer__content-user')
                answer_content = answer.get_text('\n', strip=True)
            #Illegal character 필터링
            question_title= ILLEGAL_CHARACTERS_RE.sub(r'', question_title)
            question_content= ILLEGAL_CHARACTERS_RE.sub(r'', question_content)
            answer_content= ILLEGAL_CHARACTERS_RE.sub(r'', answer_content)
            ws.append([question_title, question_content, answer_content])
            print(f'{question_title} 저장 완료', page)
            count += 1
        
    wb.save(f'{filename}_{filecount}_1.xlsx')
    print(f'{filename} 저장 완료')
    filecount+=1
#except:
#    wb.save(f'{filename}.xlsx')
#    print(f'{filename} 저장 완료')
        



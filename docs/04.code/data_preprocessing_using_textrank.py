# -*- coding: utf-8 -*-
import pandas as pd
import re
import openpyxl
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import os
from gensim.summarization import keywords, summarize

def textrank_summarize(text, ratio=0.3):
    # 문장에서 키워드를 추출합니다.
    # 키워드는 중요한 단어들을 나타냅니다.
    keywords_list = keywords(text, words=5, lemmatize=True).split('\n.?!')
    keywords_set = set(keywords_list)

    # 문장들을 문장 리스트로 변환합니다.
    sentences = text.split('.')

    # 텍스트 랭크를 적용하여 문장들의 중요도를 계산합니다.
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        sentence_scores[i] = 0
        words = sentence.split()
        for word in words:
            if word in keywords_set:
                sentence_scores[i] += 1

    # 문장들을 중요도에 따라 정렬합니다.
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)

    # 상위 순위 문장들을 선택하여 요약문을 생성합니다.
    if int(len(sentences) * ratio)<3:
        num_sentences = 3
    else:
        num_sentences = int(len(sentences) * ratio)
    selected_sentences = sorted(sorted_sentences[:num_sentences])

    # 요약문 생성
    summarized_text = '. '.join(sentences[i] for i, _ in selected_sentences)
    
    return summarized_text




keywords_list = ['http', '냠냠', 'HTML', '{', '}', '영어 문법', '닥치', '사진', 'www', '02', '031', 
                 '032', '033', '041', '042', '043', '044', '051', '052', '051', '052', '053', '054', 
                 '055', '061', '062' , '063', '064']
endkeywords = ['.', '!', '?', "\"", "\'"]

wb = openpyxl.Workbook()
ws = wb.active
ws.append(['질문', '답변'])
# 엑셀 파일 읽기
##for i in range(1, 17):
    
data = pd.read_excel('all.xlsx')

for index, row in data.iterrows():
    try:
        title = row['제목']
        content = row['질문']
        answer = row['답변']
        pattern = re.compile(r'|'.join(keywords_list))
        
        if re.search(pattern, answer):
            print(f"필터링 완료, {index}\n") #특정 키워드가 들어간 답변 제외
            continue
        if re.search(pattern, content):
            print(f"필터링 완료, {index}\n") #특정 키워드가 들어간 답변 제외
            continue
        
        pattern = re.compile(re.escape(title)) #제목과 질문이 중복되는가 확인
        match = pattern.search(content)
        pattern = re.compile(r'내공\d+') #내공100 등의 단어 제거
        title = re.sub(pattern, '', title) 
        content = re.sub(pattern, '', content) 
            
        #특정 문구로 시작하는 경우 특정 문구만 제거 
        pattern = re.escape('안녕하세요.')
        title = re.sub(pattern, '', title) 
        answer = re.sub(pattern, '', answer)
        
        if match:
            print("질문에 제목이 포함되어 있습니다.")
        else:
            content = title +' '+ content
        
        for keyword in endkeywords: #답변이 특정 문장 부호로 끝나면 통과
                if answer.endswith(keyword):
                    answer_summarized = textrank_summarize(answer)
                    if answer_summarized == '.':
                        continue
                    ws.append([content, answer_summarized])
                    print('추가됨', index)     
    except Exception as ex:
        print(index, ex)
        wb.save(f'all_error.xlsx')
        continue
wb.save('all_sum.xlsx')
print('저장 완료')
    
import pandas as pd
import re
import openpyxl
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import os
import openai

openai.api_key = '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'

def summarize_text(qeustion, answer):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a person who summarizes answers to questions. I will show you the question and answer, so please summarize the answer or add content if necessary. However, you can exclude promotional phrases, self-introducing sentences, and swear words. Please write the answer in Korean."},
            {"role": "user", "content": answer},
            {"role": "assistant", "content": qeustion}    
    ]
)
    
    return response.choices[0].message['content']
# 엑셀 파일 읽기
#for i in range(4, 12):
wb = openpyxl.Workbook()
ws = wb.active
ws.append(['질문', '답변'])
data = pd.read_excel(f'all.xlsx')

for index, row in data.iterrows():
    if index > 57000:
        try:
            title = row['제목']
            content = row['질문']
            answer = row['답변']
            
            pattern = re.compile(re.escape(title)) #제목과 질문이 중복되는가 확인
            match = pattern.search(content)

            if match:
                print("질문에 제목이 포함되어 있습니다.")
            else:
                content = title +' '+ content
            answer = summarize_text(content, answer)        
            ws.append([content, answer])
            print(answer, index)
        except Exception as ex:
            print(index, ex)
            continue
        if(index % 1000 == 0) :
            wb.save(f'all_{index}.xlsx')
wb.save(f'all_end.xlsx')
print('저장 완료')
    
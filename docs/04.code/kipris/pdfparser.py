#-*- coding: utf-8 -*-
from pdfminer.high_level import extract_text
i = 1
query = input()

# PDF ���� ���� ��ŭ ���� ����
while i <= 4238:
    # �ѹ����� �´� ������ ��� ����
    try:
        # PDF ������ �ִ� ���丮
        text = extract_text("C:/Users\choi4/source/repos/kipriscrawling/kipriscrawling/%s%d.pdf" % (query, i))
        # TXT ������ ������ ���丮
        f = open("C:/Users/choi4/Desktop/TEXTDATA/%s/%s%d.txt" % (query, query, i), 'w')
        f.write(text)
        f.close()
        i = i+1

    except FileNotFoundError as e:
        print(e)
        i = i+1

    except:
        print("ERROR")
        i = i+1
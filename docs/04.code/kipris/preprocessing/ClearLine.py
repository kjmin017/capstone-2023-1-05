
#-*- coding: utf-8 -*-
i = 1
query = input()

# PDF ���� ���� ��ŭ ���� ����
while i <= 10000:
    # �ѹ����� �´� ������ ��� ����
    try:
        lines = []
        f = open('C:/Users/choi4/Desktop/TEXTDATA/%s/%s%d.txt' % (query, query, i), "r")
        for line in f:
            if not line.isspace():
                lines.append(line)
        f.close()

        a = open('C:/Users/choi4/Desktop/AFTERTEXTDATA/%s/%s%d.txt' % (query, query, i), "w")
        for line in lines:
            a.write(line)
        a.close

        i = i+1

    except FileNotFoundError as e:
        print(e)
        i = i+1

    except:
        print("ERROR")
        i = i+1
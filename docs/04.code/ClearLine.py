
#-*- coding: utf-8 -*-
i = 1
query = input()

# PDF 파일 갯수 만큼 변수 조절
while i <= 10000:
    # 넘버링에 맞는 파일이 없어도 실행
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
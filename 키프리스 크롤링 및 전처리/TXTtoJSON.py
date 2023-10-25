# -*- coding: utf-8 -*-

from email import errors
from http.client import FOUND
import json
from collections import OrderedDict

j = 1
query = input()

while j <= 6000:
    try:
        file_data = OrderedDict()
        a = []
        f = open('C:/Users/choi4/Desktop/AFTERTEXTDATA/%s/%s%d.txt' % (query, query, j), "r")
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n", "")
            a.append(line)
        f.close()

        found_kor = a.index('【발명(고안)의 국문명칭】')
        found_eng = a.index('【발명(고안)의 영문명칭】')
        found_sum = a.index('【요약서】')
        found_pri = a.index('【대표도】')
        found_inv = a.index('【발명(고안)자】')


        applicant_list = list()
        agent_list = list()
        invent_list = list()


        kor_name = a[found_kor+1 : found_eng]
        file_data["발명(고안)의 국문명칭"] = '%s' % (kor_name)


        eng_name = a[found_eng+1 : found_inv]
        file_data["발명(고안)의 영문명칭"] = '%s' % (eng_name)


        found_app = list(filter(lambda x: a[x] == '【출원인】', range(len(a))))
        for i in found_app:
            applicant = a[i+2]
            if a[i-1] == '【지분】':
                applicant = a[i+3]
            if applicant == '특허출원서':
                applicant = a[i+5]
            applicant_num = a[a.index(applicant)+2]
            applicant_list.append({"명칭" : '%s' % (applicant), "특허고객번호" : '%s' % (applicant_num)})
        file_data['출원인'] = applicant_list


        found_age = list(filter(lambda x: a[x] == '【대리인번호】', range(len(a))))
        for i in found_age:
            agent = a[i-1]
            agent_num = a[i+1]
            agent_list.append({"명칭" : '%s' % (agent), "대리인번호" : '%s' % (agent_num)})
        file_data["대리인"] = agent_list
    

        found_inv = list(filter(lambda x: a[x] == '【발명(고안)자】', range(len(a))))
        for i in found_inv:
            invent = a[i+2]
            invent_list.append({"명칭" : '%s' % (invent)})
        file_data["발명(고안)자"] = invent_list


        summary = a[found_sum+1 : found_pri]
        file_data["요약서"] = '%s' % (summary)


        with open('C:/Users/choi4/Desktop/JSONDATA/%s/%s%d.json' % (query, query, j), 'w', encoding="utf-8") as make_file:
            json.dump(file_data, make_file, ensure_ascii=False, indent='\t')
        j = j+1


    except FileNotFoundError as e:
        print(e)
        j = j+1


    except:
        print("ERROR")
        j = j+1
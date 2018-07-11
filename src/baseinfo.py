# coding=utf-8
import re
import numpy as np
import requests
import time
from bs4 import BeautifulSoup
import json
import csv
 

s=requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

headers['Cookie'] = '_ga=GA1.2.615590818.1530446650; _gid=GA1.2.262591004.1530446650; gr_user_id=3d9d036f-2ba6-436d-82ca-2951a69f27fa; gr_cs1_093321ca-fb15-49d8-847c-bdde30e87658=user_id%3Anull; Hm_lvt_a00f46563afb7c779eef47b5de48fcde=1530446651; Qs_lvt_181814=1530446654; mediav=%7B%22eid%22%3A%22301358%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22Rha.O%5ET%3Cok%3AuX.u1sV5_%22%2C%22ctn%22%3A%22%22%7D; renrendaiUsername=17625365001; activeTimestamp=8603717; IS_MOBLIE_IDPASS=true-false; jforumUserInfo=LvemPGg7BNsOVQCdYRIXpuzIoOGkI6NZ%0A; we_token=Slo5MjE3MktwbDBPVElVdWYzbENIRUZGRi1Jb0dlUXg6ODYwMzcxNzpiOWVjODM1OTljY2E2YTZmZTZkZTVmODA1YWNmYjA1NTk2NWZjOGY0; we_sid=s%3ABXS_CK2e7B0USj2OXqO46jfp3Y7dQHLs.SgPEFpIb41J6ZCv12Dhwmck0cGeyq%2BSVaIgSsxAjhH4; Qs_pv_181814=3506823808955352000%2C467662212501409660%2C3666048921685141500; _zg=%7B%22uuid%22%3A%20%2216455bab4341d3-03d0d113e51d9e-16386952-13c680-16455bab43595%22%2C%22sid%22%3A%201530446656568%2C%22updated%22%3A%201530446826484%2C%22info%22%3A%201530446656570%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%228603717%22%7D; gr_cs1_f13f8e8a-2fac-451a-a245-8333db57b845=user_id%3A8603717; Hm_lpvt_a00f46563afb7c779eef47b5de48fcde=1530446827; gr_session_id_bf0acacc0a738790=f13f8e8a-2fac-451a-a245-8333db57b845_true; JSESSIONID=AD6728A8B8E87A082616F989162844B3'

def parse_userinfo(writer, loanid): 
    try:
        urll = "https://www.renrendai.com/loan-{loan_id}.html".format(loan_id=loanid)
        #print(urll)
        result = s.get(urll, headers=headers, timeout=1)
        print( result, urll)
        html = BeautifulSoup(result.text, 'lxml')


        script = html.findAll("script")
        info_select = re.compile(r"var info =.*?}';$", re.MULTILINE | re.DOTALL)
        detail_select=re.compile(r"var detail.*?}';$", re.MULTILINE | re.DOTALL)
        json_start_end = re.compile(r"{\\u0022.*\\u0022]}}")
        json_start_end2 = re.compile(r"{\\u0022.*}';")
        info = info_select.search(script[13].text).group()
        json_info_str = json_start_end.search(info).group()
        json_info_without_uni0022 = json_info_str.replace("\\u0022", "\"")
        json_info_without_unicode = json_info_without_uni0022.replace("\\u005C", "\\")
        #print(json_info_without_unicode)

        script = html.findAll("script")
        detail=detail_select.search(script[13].text).group()
        #print(detail)
        json_detail_str=json_start_end2.search(detail).group()
        json_detail_without_uni0022=json_detail_str.replace("\\u0022", "\"")
        json_detail_without_unicode=json_detail_without_uni0022.replace("\\u005C", "\\")[:-2]

        #print(json_detail_without_unicode)
        json_info=json.loads(json_info_without_unicode)
        json_detail=json.loads(json_detail_without_unicode)

        writer.writerow([loanid,
                        json_detail["loan"]["amount"],
                        json_detail["loan"]["interest"],
                        json_detail["loan"]["months"], #4
                        json_detail["loan"]["description"],
                        json_detail["loan"]["status"],
                        json_detail["loan"]["openTime"],
                        json_detail["loan"]["startTime"], #8
                        json_detail["loan"]["verifyState"],
                        json_info["borrower"]["userId"],
                        json_info["borrower"]["province"],
                        json_info["borrower"]["city"],#12
                        json_info["borrower"]["birthDay"],
                        json_info["borrower"]["graduation"],
                        json_info["borrower"]["idNo"],
                        json_info["borrower"]["gender"],#16
                        json_info["borrower"]["marriage"],
                        json_info["borrower"]["salary"],
                        json_info["borrower"]["hasHouse"],
                        json_info["borrower"]["houseLoan"],#20
                        json_info["borrower"]["hasCar"],
                        json_info["borrower"]["carLoan"],
                        json_info["borrower"]["creditLevel"],
                        json_info["creditInfo"]["identificationScanning"],#24
                        json_info["creditInfo"]["credit"],
                        json_info["creditInfo"]["work"],
                        json_info["creditInfo"]["incomeDuty"],
                        json_info["creditInfo"]["fieldAudit"]])#28
        return True
    except Exception as err:
        print(err)
        return False

user_info = ['loan_id', 'amount', 'interset', 'months',
             'description', 'status', 'open_time', 'start_time',
             'verify_state', 'user_id', 'province', 'city',
             'birth_day', 'graduation', 'id_no', 'gender',
             'marriage', 'salary', 'has_house', 'house_loan',
             'has_car', 'car_loan', 'credit_level', 'identification_scanning',
             'credit', 'work', 'income_duty', 'field_audit']
 


for k in range(597, 731):
    t0 = time.time()
    file_index = k * 1000
    filename = "/Users/lacdon/Dropbox/renrendai/renrendai{index}.csv".format(index=file_index)
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(user_info)
        for i in range(0, 1000):
            page_index = k * 1000 + i
            if parse_userinfo(writer, page_index):
                time.sleep(0.01)
            else:
                continue
    t1 = time.time()
    print("spend time :", t1 - t0)
    csvfile.close()



for k in range(731, 809):
    t0 = time.time()
    file_index = k * 1000
    filename = "/Users/lacdon/Dropbox/renrendai/renrendai{index}.csv".format(index=file_index)
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(user_info)
        for i in range(0, 1000):
            page_index = k * 1000 + i
            if parse_userinfo(writer, page_index):
                time.sleep(0.01)
            else:
                continue
    t1 = time.time()
    print("spend time :", t1 - t0)
    csvfile.close()


for k in range(2000, 2059):
    t0 = time.time()
    file_index = k * 1000
    filename = "/Users/lacdon/Dropbox/renrendai/renrendai{index}.csv".format(index=file_index)
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(user_info)
        for i in range(0, 1000):
            page_index = k * 1000 + i
            if parse_userinfo(writer, page_index):
                time.sleep(0.01)
            else:
                continue
    t1 = time.time()
    print("spend time :", t1 - t0)
    csvfile.close()


for k in range(2059, 2196):
    t0 = time.time()
    file_index = k * 1000
    filename = "/Users/lacdon/Dropbox/renrendai/renrendai{index}.csv".format(index=file_index)
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(user_info)
        for i in range(0, 1000):
            page_index = k * 1000 + i
            if parse_userinfo(writer, page_index):
                time.sleep(0.01)
            else:
                continue
    t1 = time.time()
    print("spend time :", t1 - t0)
    csvfile.close()
        
      
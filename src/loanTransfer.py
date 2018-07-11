# coding=utf-8

import requests
import json
import time
import csv

# Loan transfered data is an AJAX request. So just send a HTTP get message.

user_info = ['loadID', 'totalUnRepaid', 'totalRePaid', 'ID',
            'repayTime', 'repayTimeStamp', 'repaidAmount',
            'unRepaidAmount', 'repaidFee', 'unRepaidFee',
            'status', 'repayType', 'actualRepayTime', "actualRepayTimeStamp"]
            
def jsonToCsv(strJson, loanID, filePath):
    jsonData = json.loads(strJson, encoding='utf-8')
    data = jsonData["data"]
    payList = data["list"]
    if len(payList) is 0:
        return
    with open(filePath, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(user_info)
        for i in range(0, len(payList)):
            rt = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(payList[i]["repayTime"] / 1000))
            art = ""
            if payList[i]["actualRepayTime"] is None:
                art = ""
            else:
                art = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(payList[i]["actualRepayTime"] / 1000))
            writer.writerow([loanID,
                           data["unRepaid"],
                           data["repaid"],
                           payList[i]["id"],
                           rt,
                           payList[i]["repayTime"],
                           payList[i]["repaidAmount"],
                           payList[i]["unRepaidAmount"],
                           payList[i]["repaidFee"],
                           payList[i]["unRepaidFee"],
                           payList[i]["status"],
                           payList[i]["repayType"],
                           art,
                           payList[i]["actualRepayTime"]])
        csvfile.close()

def crawlSinglePage(pageIndes):
    url = "https://www.renrendai.com/transfer/detail/loanTransferred?loanId={index}".format(index=pageIndes)
    r = requests.get(url)
    if r.status_code == 200:
        return r.content.decode('utf-8')
    else:
        print(r)
        return ""
for i in range(606099, 731815):
    try :
        filename = "/Users/lacdon/Dropbox/renrendai/lt/loanTransfer-{id}.csv".format(id = i)
        jsonstr = crawlSinglePage(i)
        if len(jsonstr) is not 0 :
            print("success {id}".format(id = i))
            jsonToCsv(jsonstr, i, filename)
            time.sleep(0.2)
    except Exception as err:
        print(err)




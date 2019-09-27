from csvReader import CsvReader
from regexChecker import RegexChecker as rc
from textChecker import TextChecker as tc
import re
import pandas as pd

if __name__=="__main__":
    path = "C:\\Users\\Ko.In\\Desktop\\testdata.csv"
    reader = CsvReader(path)
    filtered_df = CsvReader.filtered_df(reader.df)

    msgs = list(filtered_df["本文[msg.body]"]) #TODO: something is wrong with the index, maybe should use get_column
    print(msgs)

    email_regex = rc.email_regex()
    phone_regex = rc.phone_regex()
    emails = []
    phones = []

    match = False
    row = {}
    result = []
    count = 0
    while count < len(msgs):
        email = re.findall(email_regex, msgs[count])
        phone = re.findall(phone_regex, msgs[count])
        if len(email) > 0:
            row["emails"] = email
            match = True
        if len(phone) > 0:
            phones.append(phone)
            row["phones"] = phone
            match = True

        if match == True:
            row["roomId"] = list(filtered_df["ルームID[msg.roomId]"])[count]
            row["msgId"] = list(filtered_df["メッセージID[msg._id]"])[count]
            row["msg"] = msgs[count]
        if not row:
            result.append(row)
        count += 1
    # print(emails)
    # print(phones)
    output_df = pd.DataFrame(result)
    print(output_df)

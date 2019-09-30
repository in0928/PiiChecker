from csvReader import CsvReader
from regexChecker import RegexChecker as rc
from textChecker import TextChecker as tc
import re
import pandas as pd

if __name__=="__main__":
    # pandas display option to show full df
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # path = "C:\\Users\\Ko.In\\Desktop\\testdata.csv"
    path = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\callcenter_data201809.csv"
    reader = CsvReader(path)
    filtered_df = CsvReader.filtered_df(reader.df)

    msgs = list(filtered_df["本文[msg.body]"])

    email_regex = rc.email_regex()
    phone_regex = rc.phone_regex()

    result = []
    count = 0
    while count < len(msgs):
        match = False
        row = {}
        email = re.findall(email_regex, msgs[count])
        phone = re.findall(phone_regex, msgs[count])
        if len(email) > 0:
            row["Email"] = email
            match = True
        if len(phone) > 0:
            row["Phone"] = phone
            match = True

        name = tc.checkName(msgs[count])
        if len(name) > 0:
            row["Name"] = name
            match = True

        address = tc.checkAddress(msgs[count])
        if len(address) > 0:
            print(address)
            row["Address"] = address
            match = True

        if match == True:
            row["RoomId"] = list(filtered_df["ルームID[msg.roomId]"])[count]
            row["MsgId"] = list(filtered_df["メッセージID[msg._id]"])[count]
            row["Msg"] = msgs[count]
            result.append(row)

        count += 1

    output_df = pd.DataFrame(result)
    print(output_df)

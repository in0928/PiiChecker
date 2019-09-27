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

    result = []
    count = 0
    while count < len(msgs):
        match = False
        row = {}
        email = re.findall(email_regex, msgs[count])
        phone = re.findall(phone_regex, msgs[count])
        if len(email) > 0:
            row["Emails"] = email
            match = True
        if len(phone) > 0:
            row["Phones"] = phone
            match = True

        if match == True:
            row["RoomId"] = list(filtered_df["ルームID[msg.roomId]"])[count]
            row["MsgId"] = list(filtered_df["メッセージID[msg._id]"])[count]
            row["Msg"] = msgs[count]
            result.append(row)

        count += 1

    output_df = pd.DataFrame(result)
    print(output_df)

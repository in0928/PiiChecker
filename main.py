import spacy

from csvReader import CsvReader
from regexChecker import RegexChecker as rc
from textChecker import TextChecker as tc
import re
import pandas as pd
import neologdn
import time

if __name__=="__main__":
    start_time = time.time()
    # pandas display option to show full df
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    # path = "C:\\Users\\Ko.In\\Desktop\\testdata.csv"
    path = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\callcenter_data (201809).csv"
    # path = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\callcenter_data (201809)partial3000.csv"
    encode = CsvReader.find_encoding(path)
    reader = CsvReader(path, encode)
    filtered_df = CsvReader.filtered_df(reader.df)

    msgs = list(filtered_df["本文[msg.body]"])

    email_regex = rc.email_regex()
    phone_regex = rc.phone_regex()

    result = []
    count = 0
    error = {}
    while count < len(msgs)-79500:
        match = False
        row = {}
        if not isinstance(msgs[count], str):
            msgs[count] = str(msgs[count])
        try:
            text = CsvReader.pre_process(msgs[count])
            nlp = spacy.load('ja_ginza_nopn', disable=["tagger", "parser", "ner", "textcat"])
            email = re.findall(email_regex, text)
            phone = re.findall(phone_regex, text)
            text = nlp(text)
            if len(email) > 0:
                print(email)
                row["Email"] = email
                match = True

            for p in phone:
                if len(p) < 10 or len(p) > 11: #TODO: think about hyphen
                    phone.remove(p)
            if len(phone) > 0:
                print(phone)
                row["Phone"] = phone
                match = True

            name = tc.checkName(text)
            if len(name) > 0:
                print(name)
                row["Name"] = name
                match = True

            address = tc.checkAddress(text)
            if len(address) > 0:
                print(address)
                row["Address"] = address
                match = True

        except Exception as e:
            error[count] = str(e)

        if match == True:
            row["RoomId"] = list(filtered_df["ルームID[msg.roomId]"])[count]
            row["MsgId"] = list(filtered_df["メッセージID[msg._id]"])[count]
            row["Msg"] = msgs[count]
            result.append(row)
        count += 1

    output_df = pd.DataFrame(result)
    print(output_df)
    if error:
        print(error)

    print("--- %s seconds ---" % (time.time() - start_time))

import spacy
from toolBox import *
from regexChecker import RegexChecker as rc
from textChecker import TextChecker as tc
import re
import pandas as pd
import time

if __name__=="__main__":
    start_time = time.time()

    # pandas display option to show full df
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    #TODO: add length option to show all

    nlp = spacy.load('ja_ginza_nopn', disable=["tagger", "parser", "ner", "textcat"])
    stop_file = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\StopKey_pii.csv"
    add_stop_words(read_to_list(stop_file, find_encoding(stop_file)), nlp)

    file = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\callcenter_data (201809).csv"
    filtered_df = filtered_df(read_to_df(file, find_encoding(file)))

    raw_msgs = list(filtered_df["本文[msg.body]"])
    new_msgs = pre_process(raw_msgs)
    email_regex = rc.email_regex()
    phone_regex = rc.phone_regex()

    result = []
    count = 0
    error = {}

    docs = nlp.pipe(new_msgs)
    print("Entering loop")

    for msg in docs:
        match = False
        row = {}

        email = re.findall(email_regex, str(msg))
        phone = re.findall(phone_regex, str(msg))
        if len(email) > 0:
            print("Found email at " + str(count) + ": " + ",".join([str(n) for n in email]))
            row["Email"] = email
            match = True

        for p in phone:
            p = str(p)
            if len(p) < 10 or len(p) > 11: #TODO: think about hyphen
                phone.remove(p)
        if len(phone) > 0:
            print("Found phone at " + str(count) + ": " + ",".join([str(n) for n in phone]))
            row["Phone"] = phone
            match = True

        name = tc.checkName(msg)
        if len(name) > 0:
            print("Found name at " + str(count) + ": " + ",".join([str(n) for n in name]))
            row["Name"] = name
            match = True

        address = tc.checkAddress(msg)
        if len(address) > 0:
            print("Found address at " + str(count) + ": " + ",".join([str(n) for n in address]))
            row["Address"] = address
            match = True


        if match == True:
            row["RoomId"] = list(filtered_df["ルームID[msg.roomId]"])[count]
            row["MsgId"] = list(filtered_df["メッセージID[msg._id]"])[count]
            row["Msg"] = raw_msgs[count]
            result.append(row)
        count += 1

    output_df = pd.DataFrame(result)
    print(output_df)
    if error:
        print(error)

    print("--- %s seconds ---" % (time.time() - start_time))

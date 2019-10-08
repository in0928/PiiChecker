import codecs
import os
import random
import string
from pathlib import Path
import pandas as pd
import toolBox

data_folder = Path("data/")
name_data_folder = Path("data/name/")
location_data_folder = Path("data/location/")
email_quant = 20
name_quant = 500
location_quant = 10
phone_quant = 10
data_quant = 100
random_num = random.randint(5,20)


def create_email():
    dot = "."
    underscore = "_"
    count = 0
    c = 0
    emails = []
    file = data_folder / "free_email_provider_domains.txt"
    with open(file, "r") as f:
        lineList = f.readlines()
    lineList = [line.rstrip('\n') for line in lineList]

    while count < email_quant:
        random_len = random.randint(5,15)
        random_index = random.randint(0, len(lineList)-1)
        prefix = random.SystemRandom().choice(string.ascii_letters)
        suffix = random.SystemRandom().choice(string.ascii_letters)
        temp_str = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + dot + underscore + "\n") for _ in range(random_len))

        random_str = prefix + temp_str + suffix
        email = random_str + "@" + lineList[random_index]
        emails.append(email)

        count += 1

    return emails


def create_name(header):
    fullName_kanji_list = []
    fullName_mix_list = []
    firstName_file = name_data_folder / "M95_MEI.TXT"
    lastName_file = name_data_folder / "M95_SEI.TXT"

    with codecs.open(firstName_file, "r", toolBox.find_encoding(firstName_file), "ignore") as f:
        first_df = pd.read_table(f, delimiter="\t", header=header)
        firstName_kanji_list = list(first_df[1])
        firstName_hira_list = list(first_df[0])

    with codecs.open(lastName_file, "r", toolBox.find_encoding(lastName_file), "ignore") as f:
        last_df = pd.read_table(f, delimiter="\t", header=header)
        lastName_kanji_list = list(last_df[1])[:-1]
        lastName_hira_list = list(last_df[0])[:-1]

    i = 0
    while i < name_quant:
        lastName_kanji_index = random.randint(0, len(lastName_kanji_list) - 1)
        firstName_kanji_index = random.randint(0, len(firstName_kanji_list) - 1)
        firstName_hira_index = random.randint(0, len(firstName_hira_list) - 1)
        kanji_name = "".join([str(lastName_kanji_list[lastName_kanji_index]), str(firstName_kanji_list[firstName_kanji_index])])
        mix_name = "".join([str(lastName_kanji_list[lastName_kanji_index]), str(firstName_hira_list[firstName_hira_index])])
        fullName_kanji_list.append(kanji_name)
        fullName_mix_list.append(mix_name)
        i += 1
    return fullName_kanji_list, fullName_mix_list, lastName_kanji_list, lastName_hira_list, firstName_kanji_list, firstName_hira_list

def create_location():
    address = []

    for file in os.listdir(location_data_folder):
        with codecs.open(file, "r", toolBox.find_encoding(file), "ignore") as f:
            df = pd.read_table(f, delimiter="\t", header=None)
            firstName_kanji_list = list(first_df[1])
    return address

def create_phone_number():
    hyphen = "-"
    phones = []
    count = 0
    while count < phone_quant:
        random_len = random.randint(9, 11)
        # add_hyphen = random.choice([True, False])
        temp_phone = ''.join(random.SystemRandom().choice(string.digits) for _ in range(random_len))
        random_phone = "0" + temp_phone
        phones.append(random_phone)
        count += 1
    return phones


def add_text(some_list):
    text_pattern = ["あいうえお", "カキクケッコ", "日本語", "１２３", "456", "Ｅｎｇｌｉｓｈ", "Awesome", " ", "　"]
    new_list = []
    count = 0
    for i in some_list:
        random_index = random.randint(0, len(text_pattern)-1)
        if count > len(text_pattern) -1:
            count = count - len(text_pattern) -1
        new_i = text_pattern[count] + str(i) + text_pattern[random_index]
        new_list.append(new_i)
        count += 1
    return new_list


def write_to_csv_for_test(list_of_rows, filename):
    df = pd.DataFrame(list_of_rows)
    # print(df)

    # df = df.reindex(label, axis=1)
    df.to_csv(filename, sep="\t", index=False, header=None)
    print("Successfully wrote df to csv file")


if __name__ == "__main__":
    print(create_location())

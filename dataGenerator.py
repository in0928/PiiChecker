import random
import string
from pathlib import Path
import pandas as pd

data_folder = Path("data/")
email_quant = 20
name_quant = 10
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


def create_name():
    firstName = []
    lastName = []
    fullname = []
    firstName_file = data_folder / "M95_MEI.TXT"
    lastName_file = data_folder / "M95_SEI.TXT"
    with open(firstName_file, "r") as first_file:
        first_list = first_file.readlines()
    first_list = [line.rstrip('\n') for line in first_list]

    with open(lastName_file, "r") as last_file:
        last_list = last_file.readlines()
    last_list = [line.rstrip('\n') for line in last_list]

def create_location():
    pass

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
    print(df)

    # df = df.reindex(label, axis=1)
    df.to_csv(filename, sep="\t", index=False, header=None)
    print("Successfully wrote df to csv file")


if __name__ == "__main__":
    # print(create_email())
    # print(create_phone_number())
    emails = create_email()
    modified_emails = add_text(emails)
    print(modified_emails)

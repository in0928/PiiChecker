import time
from pathlib import Path
import dataGenerator as dg
from regexChecker import RegexChecker as rc
from toolBox import *

if __name__=="__main__":
    data_folder = Path("data/")
    file = data_folder / "email_test.csv"

    test_emails = dg.create_email()
    modified_emails = dg.add_text(test_emails)
    dg.write_to_csv_for_test(modified_emails, file)

    expected_emails = dg.email_quant
    print("There are " + str(expected_emails) + " email entities")

    time.sleep(3)

    nlp = spacy.load('ja_ginza_nopn', disable=["tagger", "parser", "ner", "textcat"])
    stop_file = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\StopKey_pii.csv"
    add_stop_words(read_to_list(stop_file, find_encoding(stop_file)), nlp)
    df = read_to_df(file, find_encoding(file))

    raw_msgs = list(df[0])

    new_msgs = pre_process(raw_msgs)

    email_regex = rc.email_regex()
    phone_regex = rc.phone_regex()

    result = []
    count = 0

    docs = nlp.pipe(new_msgs)

    for msg in docs:
        match = False
        row = {}

        email = re.findall(email_regex, str(msg))
        if len(email) > 0:
            print("Found email at " + str(count) + ": " + ",".join([str(n) for n in email]))
            row["Email"] = "".join([str(n) for n in email])
            match = True

        if match == True:
            result.append(row)
        count += 1

    output_df = pd.DataFrame(result)
    print(output_df)

    actual_emails = len(output_df.index)
    print("The actual detected emails entities are: " + str(actual_emails))
    print("Accuracy of email extraction is: " + str(actual_emails/expected_emails))

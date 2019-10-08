import time
from pathlib import Path
import dataGenerator as dg
from textChecker import TextChecker as tc
from toolBox import *

def run_test(name_list, test_filename, nlp):
    print("Starting test for " + test_filename)
    data_folder = dg.name_data_folder
    test_file = data_folder / test_filename
    dg.write_to_csv_for_test(name_list, test_file)
    df = read_to_df(test_file, find_encoding(test_file))
    raw_msgs = list(df[0])
    new_msgs = pre_process(raw_msgs)
    expected_output = len(name_list)
    print("There are " + str(expected_output) + " entities")
    time.sleep(3)
    docs = nlp.pipe(new_msgs)
    result = []
    count = 0
    for msg in docs:
        match = False
        row = {}
        name = tc.checkName(msg)
        if len(name) > 0:
            temp_name = str(name[0])
            if temp_name == new_msgs[count]:
                # print("Found name at " + str(count) + ": " + temp_name)
                row["Name"] = temp_name
                match = True
            else:
                print("Partially detected at " + str(count) + ": " + new_msgs[count])
        else:
            print("Not recognized at " + str(count) + ": " + new_msgs[count])
        if match == True:
            result.append(row)
        count += 1
    output_df = pd.DataFrame(result)
    # print(output_df)
    actual_output = len(output_df.index)
    print("The actual detected entities are: " + str(actual_output))
    accuracy = actual_output/expected_output
    print("Accuracy of extraction is: " + str(accuracy))
    return accuracy


if __name__=="__main__":
    pd.set_option('display.max_rows', 1500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_colwidth', 150)
    pd.set_option('display.width', 1000)
    test_data = dg.create_name(header=None)
    fullKanjiName = test_data[0]
    fullMixName = test_data[1]
    lastKanjiName = test_data[2]
    lastHiraName = test_data[3]
    firstKanjiName = test_data[4]
    firstHiraName = test_data[5]

    nlp = spacy.load('ja_ginza_nopn', disable=["tagger", "parser", "ner", "textcat"])
    stop_file = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\StopKey_pii.csv"
    add_stop_words(read_to_list(stop_file, find_encoding(stop_file)), nlp)

    a_full_kanji = []
    a_full_mix = []
    a_last_kanji = []
    a_last_hira = []
    a_first_kanji = []
    a_first_hira = []

    data_folder = dg.name_data_folder
    last_hira_run = run_test(lastHiraName, "lastHiraName_test.csv", nlp)
    a_last_hira.append(last_hira_run)
    last_kanji_run = run_test(lastKanjiName, "lastKanjiName_test.csv", nlp)
    a_last_kanji.append(last_kanji_run)
    first_hira_run = run_test(firstHiraName, "firstHiraName_test.csv", nlp)
    a_first_hira.append(first_hira_run)
    first_kanji_run = run_test(firstKanjiName, "firstKanjiName_test.csv", nlp)
    a_first_kanji.append(first_kanji_run)

    test_times = 10
    run_times = 0
    while run_times < test_times:
        full_mix_run = run_test(fullMixName, "fullMixName_test.csv", nlp)
        a_full_mix.append(full_mix_run)
        full_kanji_run = run_test(fullKanjiName, "fullKanjiName_test.csv", nlp)
        a_full_kanji.append(full_kanji_run)
        run_times += 1

    print("lastName Hira Accuracy:" + str(sum(a_last_hira)/len(a_last_hira)))
    print("lastName Kanji Accuracy:" + str(sum(a_last_kanji)/len(a_last_kanji)))
    print("firstName Hira Accuracy:" + str(sum(a_first_hira)/len(a_first_hira)))
    print("firstName Kanji Accuracy:" + str(sum(a_first_kanji)/len(a_first_kanji)))
    print("fullName Mix Accuracy:" + str(sum(a_full_mix)/len(a_full_mix)))
    print("fullName Kanji Accuracy:" + str(sum(a_full_kanji)/len(a_full_kanji)))


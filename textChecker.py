import re

import neologdn
import spacy

class TextChecker:

    @staticmethod
    def checkName(nlp_sentence):
        name = []
        count = 0
        while count < len(nlp_sentence):
            if nlp_sentence[count].is_stop:
                # print("Found stop_word:" + str(nlp_sentence[count]))
                count += 1
                continue
            if nlp_sentence[count]._.pos_detail == "名詞,固有名詞,人名,姓":
                # to detect full-name
                if count < len(nlp_sentence)-1 and nlp_sentence[count+1]._.pos_detail == "名詞,固有名詞,人名,名":
                    fullName = "".join([str(nlp_sentence[count]), str(nlp_sentence[count+1])])
                    name.append(fullName)
                    print("Found fullName: " + fullName)
                    count += 1
                else:
                    lastName = str(nlp_sentence[count])
                    name.append(lastName)
                    print("Found lastName: " + lastName)
            elif nlp_sentence[count]._.pos_detail == "名詞,固有名詞,人名,名":
                firstName = str(nlp_sentence[count])
                name.append(nlp_sentence[count])
                print("Found firstName: " + firstName)
            count += 1
        return name

    @staticmethod
    def checkLocation(nlp_sentence):
        location = []
        address = []
        count = 0
        while count < len(nlp_sentence):
            if nlp_sentence[count].is_stop:
                # print("Found stop_word:" + str(nlp_sentence[count]))
                count += 1
                continue
            if nlp_sentence[count]._.pos_detail == "名詞,固有名詞,地名,一般":
                # detect all location entity
                end_index = TextChecker.target_ends_at(nlp_sentence[count+1:], "名詞,固有名詞,地名,一般") + count
                location.append(nlp_sentence[count: end_index+1])
                # following location entities exist
                if end_index > count:
                    count = end_index

                number_end_index = TextChecker.number_ends_at(nlp_sentence[count+1:]) + count
                # print("number ends at: " + str(TextChecker.number_ends_at(nlp_sentence[count+1:])))
                # print(number_end_index)
                # number entities exist
                if number_end_index > count:
                    # location.append(nlp_sentence[end_index+1: number_end_index+1])
                    [address.append(i) for i in location]
                    address.append(nlp_sentence[end_index+1: number_end_index+1])

            count += 1
        return location, address


    @staticmethod
    def number_ends_at(nlp_sentence):
        """
        1-2-3, return last index + 1
        一丁目二番地三号,　return last index + 1
        数字がない、return count = 0
        """
        count = 0
        while count < len(nlp_sentence):
            if nlp_sentence[count]._.pos_detail == "名詞,数詞,*,*":
                count += 2
                continue
            elif count > 3 and nlp_sentence[count-3]._.pos_detail == "補助記号,一般,*,*":
                print("Found address ends with number")
                return count-1
            elif count > 0 and nlp_sentence[count-1].text == "号":
                print("Found address ends with 'Gou'")
                return count
            else:
                return 0
        return count

    @staticmethod
    def target_ends_at(tokens, target):
        """
        :param tokens: a list of words which can be indexed
        :param target: _.pos_detail of the word in tokens
        :param target_ignore: _.pos_detail of token to ignore, optional
        :return: the index where the last match with target tag_ occurs
        """
        count = 0
        while count < len(tokens):
            if tokens[count]._.pos_detail == target:
                count += 1
                continue
            else:
                return count
        return count


if __name__=="__main__":
    s1 = "数字が4つで文字アドレスが複数の場合、東京都立川市港区木葉下町5-1-3-1502だよ"
    s2 = "数字が4つで文字アドレスが1つの場合、六本木5-1-3-1122だよ"
    s3 = "数字が3つで文字アドレスが複数の場合、東京都大阪市浪速区なんば5-1-3だよ"
    s4 = "数字が3つで文字アドレスが1つの場合、六本木２ー３ー３だよ"
    s7 = "数字が漢数字で文字アドレスが複数の場合、東京都立川市港区宿毛三丁目二番地五号だよ"
    s8 = "数字が漢数字で文字アドレスが複数の場合、東京都立川市港区浜松町三丁目二番地1号だよ"
    s9 = "適当に浜松三方原店に来店"
    n1 = "会野谷凝然"

    test_list = [s1,s8,s9]
    name_list = [n1]
    nlp = spacy.load('ja_ginza_nopn', disable=["tagger", "parser", "ner", "textcat"])

    for s in name_list:
        s = nlp(s)
        address = TextChecker.checkName(s)
        print(address)
        for i in s:
            print(i.text)

    # text = "お友達の紹介で、女子２人で三時のティータイムに利用しました。2人用のソファに並んでいただきま〜す v(^^)v なかよし（笑" \
    #        "最後に出された,モンブランのｹｰｷ。" \
    #        "やばっっっ！！これはうまーーーい!!" \
    #        "とってもＤｅｌｉｃｉｏｕｓで、サービスもGoodでしたAmazon😀" \
    #        "これで2,500円はとってもお得です☆" \
    #        "http://hogehoge.nantoka.blog/example/link.html"


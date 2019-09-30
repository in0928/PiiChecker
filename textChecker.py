import spacy

class TextChecker:

    @staticmethod
    def checkName(sentence):
        name = []
        nlp = spacy.load('ja_ginza_nopn')
        sent = nlp(sentence)
        count = 0
        while count < len(sent):
            if sent[count]._.pos_detail == "名詞,固有名詞,人名,姓":
                # to detect full-name
                if count < len(sent)-1 and sent[count+1]._.pos_detail == "名詞,固有名詞,人名,名":
                    name.append((sent[count], sent[count+1]))
                    count += 1
                else:
                    name.append(sent[count])
            elif sent[count]._.pos_detail == "名詞,固有名詞,人名,名":
                name.append(sent[count])
            count += 1
        return name

    @staticmethod
    def checkAddress(sentence):
        address = []
        nlp = spacy.load('ja_ginza_nopn')
        sent = nlp(sentence)
        count = 0
        while count < len(sent):
            if sent[count]._.pos_detail == "名詞,固有名詞,地名,一般":
                # detect all address entity
                end_index = TextChecker.target_ends_at(sent[count+1:], "名詞,固有名詞,地名,一般") + count
                address.append(sent[count: end_index+1])
                # following address entities exist
                if end_index > count:
                    count = end_index

                number_end_index = TextChecker.number_ends_at(sent[count+1:]) + count
                # number entities exist
                if number_end_index > count:
                    address.append(sent[end_index+1: number_end_index+1])

            count += 1

        return address

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

    @staticmethod
    def number_ends_at(tokens):
        count = 0
        while count < len(tokens):
            if tokens[count]._.pos_detail == "名詞,数詞,*,*":
                count += 2
                # print("if" + str(count))
                continue
            elif count > 0 and tokens[count-3]._.pos_detail == "補助記号,一般,*,*":
                # print("elif")
                # print(tokens[count-3:])
                return count-1
            else:
                # print("else")
                return count
        return count


if __name__=="__main__":
    s1 = "数字が4つで文字アドレスが複数の場合、東京都立川市港区上木葉下町5-1-3-1502だよ"
    s2 = "数字が4つで文字アドレスが1つの場合、六本木5-1-3-1122だよ"
    s3 = "数字が3つで文字アドレスが複数の場合、東京都大阪市浪速区なんば5-1-3だよ"
    s4 = "数字が3つで文字アドレスが1つの場合、六本木２ー３ー３だよ"
    s5 = "数字が2つで文字アドレスが複数の場合、東京都立川市港区六本木１－３だよ"
    s6 = "数字が2つで文字アドレスが1つの場合、麻布十番３－３だよ"
    s7 = "数字が漢数字で文字アドレスが複数の場合、東京都立川市港区宿毛三丁目二番地五号だよ"
    s8 = "数字が漢数字で文字アドレスが複数の場合、東京都立川市港区浜松町三丁目二番地だよ"
    s9 = "数字が漢数字で文字アドレスが1つの場合、東京都立川市港区だよ"

    test_list = [s1,s2,s3,s4,s5,s6,s7,s8,s9]

    for s in test_list:
        address = TextChecker.checkAddress(s)
        print(address)

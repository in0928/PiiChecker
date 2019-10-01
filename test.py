import spacy
import neologdn

nlp = spacy.load('ja_ginza_nopn')
doc = nlp('私は、東京都大阪市浪速区なんば5-1-3-1502だよ')
count = 0
for sent in doc.sents:
    while count < 15:
        print(sent[count].i, sent[count].orth_,sent[count]._.pos_detail)
        count += 1
import codecs
import re

import chardet
import emoji
import pandas as pd
import string
import neologdn

class CsvReader:

    def __init__(self, path, encode):
        self.df = self.load_file(path, encode)


    @staticmethod
    def load_file(path, encode):
        # col_names = ["メッセージID[msg._id]","送信時刻[msg.dateStr]","ルームID[msg.roomId]",
        #              "送信者ID[msg.userId]","システムメッセージ[msg.system]", "本文[msg.body]",
        #              "メッセージタイプ[msg.type]","メッセージデータ[msg.data]","メッセージに付随するデータ[msg.extra]",
        #              "削除フラグ[msg.removed]","削除された日時[msg.removedDate]","ルームID[room.id]",
        #              "ゲストユーザーID[room.world]","ルーム名[room.name]","オペレーターID[room.tags.1]",
        #              "分類区分1[room.tags.2]","分類区分2[room.tags.3]","ルーム終了日時[room.tags.4]",
        #              "ルームが終了した理由[room.tags.5]","分類区分3[room.tags.6]","オペレーターメモ[room.tags.7]",
        #              "問い合わせWebページ情報[room.tags.8]","ルームの自動応答状態[room.tags.9]","ゲスト評価[room.tags.10]",
        #              "ゲストの任意のコメント[room.tags.11]","オペレーター対応開始日時[room.tags.12]","最初にオペレーターが対応した日時[room.tags.13]",
        #              "最初に担当したオペレーターID[room.tags.14]","最初のメッセージの送信日時[room.tags.15]","最初にメッセージを送信したオペレーターID[room.tags.16]",
        #              "保留フラグ[room.tags.17]","保留回数[room.tags.18]","保留開始日時[room.tags.19]",
        #              "合計の保留時間[room.tags.20]","問い合わせ元情報[room.tags.21]","監視キーワードを含めたメッセージID[room.tags.22]",
        #              "一時保存情報[room.tags.23]","グループID[room.tags.24]","ルームが完了した日時[room.tags.25]",
        #              "問い合わせユーザーの外部連携ID[room.tags.26]","担当オペレーターID履歴[room.tags.27]","保留終了日時[room.tags.28]",
        #              "ルーム完了状態[room.tags.29]","PQPA[room.tags.30]","tag31[room.tags.31]",
        #              "tag32[room.tags.32]","tag33[room.tags.33]","tag34[room.tags.34]",
        #              "tag35[room.tags.35]","tag36[room.tags.36]","tag37[room.tags.37]",
        #              "tag38[room.tags.38]","tag39[room.tags.39]","tag40[room.tags.40]",
        #              "tag41[room.tags.41]","tag42[room.tags.42]","tag43[room.tags.43]",
        #              "tag44[room.tags.44]","tag45[room.tags.45]","tag46[room.tags.46]",
        #              "tag47[room.tags.47]","tag48[room.tags.48]","tag49[room.tags.49]",
        #              "tag50[room.tags.50]","tag51[room.tags.51]","tag52[room.tags.52]",
        #              "tag53[room.tags.53]","tag54[room.tags.54]","tag55[room.tags.55]",
        #              "tag56[room.tags.56]","tag57[room.tags.57]","tag58[room.tags.58]",
        #              "tag59[room.tags.59]","tag60[room.tags.60]","自動応答モジュール名[room.tags.61]",
        #              "流入元ゲストユーザー種別[room.tags.62]","メッセージ更新状況[room.tags.63]","自動翻訳設定[room.tags.64]",
        #              "流入元詳細情報[room.tags.65]","発言者のその他の情報[room.desc]","問い合わせ状態[room.extra]",
        #              "作成時日時[room.createdAtStr]","メッセージ発言者[msgUser.name]","発言者（権限別）[msgUser.permitLevel]",
        #              "ルーム担当者[roomOperator.name]","ルーム担当者（権限別）[roomOperator.permitLevel]","プラットフォーム[room.tag21Obj.platform]",
        #              "言語[room.tag21Obj.language]","時間帯[room.tag21Obj.timeZone]","リファラー[room.tag21Obj.referer]",
        #              "タイトル[room.tag21Obj.title]","バージョン[room.tag21Obj.jsVersion]","自動応答対応時間[room.descObj.autoReplyWorkingTime]",
        #              "オペレーター対応時間[room.descObj.operatorWorkingTime]","最終発言時刻[room.descObj.lastMsgTime]","分類区分1(ラベル)[room.tags.66]",
        #              "分類区分2(ラベル)[room.tags.67]","分類区分3(ラベル)[room.tags.68]","アクセス元IP[room.tags.71]",
        #              "グループ名[room.groupName]","最初に担当したオペレーター名[room.tag14UserName]","最初にメッセージを送信したオペレーター名[room.tag16UserName]"]
        with codecs.open(path, "r", encode, "ignore") as file:
            df = pd.read_table(file, delimiter="\t")
        return df

    @staticmethod
    def filtered_df(df):
        new_df = df[~df["送信者ID[msg.userId]"].str.contains("dummy-", na=False)]
        return new_df

    @staticmethod
    def find_encoding(filename):
        r_file = open(filename, 'rb').read()
        result = chardet.detect(r_file)
        charenc = result['encoding']
        return charenc

    @staticmethod
    def pre_process(input_text):
        normalized_text = neologdn.normalize(input_text)
        text_no_url = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', normalized_text)
        text_no_emoji = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in text_no_url])
        tmp = re.sub(r'[!-/:-@[-`{-~]', r' ', text_no_emoji)
        text_removed_symbol = re.sub(u'[■-♯]', ' ', tmp)
        return text_removed_symbol


if __name__=="__main__":
    # path = "C:\\Users\\Ko.In\\Desktop\\testdata.csv"
    path = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\callcenter_data (201809).csv"
    # enc = CsvReader.find_encoding(path)
    # reader = CsvReader(path)
    # print(reader.df)
    # filtered = reader.filtered_df(reader.df)
    # print(filtered)

    text = "お友達の紹介で、女子２人で三時のティータイムに利用しました。2人用のソファに並んでいただきま〜す v(^^)v なかよし（笑" \
           "最後に出された,モンブランのｹｰｷ。" \
           "やばっっっ！！これはうまーーーい!!" \
           "とってもＤｅｌｉｃｉｏｕｓで、サービスもGoodでした😀" \
           "これで2,500円はとってもお得です☆" \
           "http://hogehoge.nantoka.blog/example/link.html"
    print(CsvReader.pre_process(text))

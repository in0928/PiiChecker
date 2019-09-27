import codecs
import pandas as pd
import string

class CsvReader:

    def __init__(self, path):
        self.df = self.load_file(path)


    @staticmethod
    def load_file(path):
        with codecs.open(path, "r", "Shift-JIS", "ignore") as file:
            df = pd.read_table(file, delimiter="\t")
        return df

    @staticmethod
    def filtered_df(df):
        new_df = df[~df["送信者ID[msg.userId]"].str.contains("dummy-autoReply--asurion", na=False)]
        return new_df

    # def get_column(self, col_name):
    #     return self.df[col_name]

if __name__=="__main__":
    path = "C:\\Users\\Ko.In\\Desktop\\testdata.csv"
    reader = CsvReader(path)
    filtered = reader.filtered_df(reader.df)
    print(filtered)

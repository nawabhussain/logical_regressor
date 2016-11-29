from itertools import repeat

import pandas as pd


def write_xlsx(dataframe, name_of_file):
    writer = pd.ExcelWriter(name_of_file)
    dataframe.to_excel(writer, 'Sheet1')
    writer.save()
    print("Xlsxx Created")


# print(dataframe[(dataframe.Participant_ID == 1) & (dataframe.Sleep == 0)])
def get_sleepOnset(dataframe):
    for i in range(1, 9):
        participant_df = dataframe[(dataframe.Participant_ID == i)]
        print("Sleep onset Participant numebr ", i)
        for index, row in participant_df.iterrows():

            if index == 0:
                prev_row = row
                print(participant_df.Sleep[index])
                print(participant_df.Time[index])
            elif row.Sleep != prev_row.Sleep:
                prev_row = row
                print(participant_df.Sleep[index])
                print(participant_df.Time[index])


def get_sleepdurarion(dataframe):
    for i in range(1, 2):
        is_next_row = False
        participant_df = dataframe[(dataframe.Participant_ID == 1)]
        print("Sleep duration Participant numebr ", i)
        for index, row in participant_df.iterrows():
            if index == 0 or is_next_row:
                if row.Sleep == 1:
                    prev_row = row
                    is_next_row = False
                    print(participant_df.Sleep[index])
                    print(participant_df.Time[index])
            elif row.Sleep != prev_row.Sleep:
                if row.Sleep == 0:
                    prev_row = row
                    is_next_row = True
                    print(participant_df.Sleep[index])
                    print(participant_df.Time[index])

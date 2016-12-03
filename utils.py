import datetime
from math import nan

import math
import pandas as pd


def write_xlsx(dataframe, name_of_file):
    writer = pd.ExcelWriter(name_of_file)
    dataframe.to_excel(writer, 'Sheet1')
    writer.save()
    print("Xlsxx Created")


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
                if row.Sleep == 1:
                    print(participant_df.Sleep[index])
                    print(participant_df.Time[index])


def get_sleepdurarion(dataframe):
    for i in range(1, 2):
        is_next_row = False
        participant_df = dataframe[(dataframe.Participant_ID == i)]
        print("Sleep duration Participant numebr ", i)
        for index, row in participant_df.iterrows():
            if index == 0 or is_next_row:
                if row.Sleep == 1:
                    prev_row = row
                    prev_index = index
                    is_next_row = False
                    print(participant_df.Sleep[index])
                    print(participant_df.Time[index])
            elif row.Sleep != prev_row.Sleep:
                if row.Sleep == 0:
                    prev_row = row
                    prev_index = index
                    is_next_row = True
                    print("End Sleep row")
                    print(participant_df.Sleep[prev_index - 1])
                    print(participant_df.Time[prev_index - 1])


def get_MSF(dataframe):
    # get_sleepOnset(dataframe)
    get_sleepdurarion(dataframe)
    return


def RMSe(e, r):
    return pd.np.sqrt(pd.np.sum((((e - r) ** 2))) / len(e))


def getWorkDaysList(labels_df):
    subjectWorkDaysList = pd.DataFrame()
    for subject_id, subject_df in labels_df.groupby(labels_df.Participant_ID):
        for date_dy, date_df in subject_df.groupby(subject_df.date):
            subjectWorkDaysList = subjectWorkDaysList.append(pd.Series(
                {
                    'Subject_id': subject_id,
                    'Date': date_dy,
                    'Workday': date_df.Workday.iloc[0],
                }), ignore_index=True)

    return subjectWorkDaysList


def getSubjectSleepData(feature_df, subjectWorkDaysList):
    subjectSleepData = pd.DataFrame()
    for subject_id, subject_df in feature_df.groupby(feature_df.Subject):
        for date_day, date_df in subject_df.groupby(subject_df.date):

            SD = 0
            Workday = 0

            if (len(subjectSleepData) > 0 and
                        len(subjectSleepData.loc[
                                    subjectSleepData.Subject_id == subject_id]) > 0):
                yesterday_SO = \
                    subjectSleepData.loc[subjectSleepData.Subject_id == subject_id].SO.iloc[
                        -1]
                today_wakeup_time = min(date_df.Test_time)

                if (yesterday_SO.date() == today_wakeup_time.date() - datetime.timedelta(days=1)):
                    dif = today_wakeup_time - yesterday_SO
                    SD = dif.seconds / (60)
                    # print(subject_id)
                    # print(SD)
            workdayRow = subjectWorkDaysList.loc[(subjectWorkDaysList.Date == date_day) &
                                                 (subjectWorkDaysList.Subject_id == subject_id)]

            if (len(workdayRow.Workday.values) > 0):
                Workday = workdayRow.Workday.values[0]

            i = max(date_df.Test_time).to_pydatetime()
            subjectSleepData = subjectSleepData.append(pd.Series(
                {
                    'Subject_id': subject_id,
                    'SO': max(date_df.Test_time),
                    'SO_Sec': int((i.hour * 3600 + i.minute * 60 + i.second)),  # seconds
                    'SD': SD,  # seconds
                    'Workday': Workday
                }), ignore_index=True)

    return subjectSleepData


def getAvgSleepDuration(subjectSleepData, subject_id, workday):
    avgSD = subjectSleepData.loc[(subjectSleepData.Subject_id == subject_id) &
                                 (subjectSleepData.Workday == workday)].SD.mean()

    avgSO = subjectSleepData.loc[(subjectSleepData.Subject_id == subject_id) &
                                 (subjectSleepData.Workday == workday)].SO_Sec.mean()

    return avgSD, avgSO


def computeMSF(feature_df, labels_df):
    resultList = pd.DataFrame()

    date = labels_df.Time.apply(lambda x: x.date())
    labels_df['date'] = date

    subjectWorkDaysList = getWorkDaysList(labels_df)
    subjectSleepData = getSubjectSleepData(feature_df, subjectWorkDaysList)

    for subject_id, subject_df in subjectSleepData.groupby(subjectSleepData.Subject_id):

        avg_SD_free, avg_SO_free = getAvgSleepDuration(subjectSleepData, subject_id, 0.0)
        MSf = avg_SO_free + avg_SD_free / 2
        if (math.isnan(MSf)):
            MSf = 0.0

        avg_SD_work, avg_SO_work = getAvgSleepDuration(subjectSleepData, subject_id, 1.0)
        MSw = avg_SO_work + avg_SD_work / 2
        if (math.isnan(MSw)):
            MSw = 0.0

        SD_sum = subjectSleepData.loc[(subjectSleepData.Subject_id == subject_id)
                                      & subjectSleepData.SD != 0].SD.sum()
        SD_days = len(subjectSleepData.loc[(subjectSleepData.Subject_id == subject_id)
                                           & subjectSleepData.SD != 0].SD)

        SD_week_avg = SD_sum / SD_days

        if (avg_SD_free > SD_week_avg):
            MSF_final = MSf - (avg_SD_free - SD_week_avg) / 2
        else:
            MSF_final = MSf

        resultList = resultList.append(pd.Series(
            {
                "Subject_id": subject_id,
                "MSF": MSf,
                "MSW": MSw,
                "MSF_final": MSF_final
            }), ignore_index=True);

    return resultList.MSW

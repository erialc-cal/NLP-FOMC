import pandas as pd
import datetime
import matplotlib.pyplot as plt
import ast


project_directory = '/Users/etiennelenaour/Desktop/Stage/'
l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']
l_dates = list()


with open ('/Users/etiennelenaour/Desktop/Stage/csv_files/dates_fomc.csv', 'r') as doc :
    head = doc.readline()
    dates = doc.readlines()
    dates_to_chg = []
    for line in dates :
        if line.split(',')[1] == ' Y' :
            dates_to_chg += [line.split(';')[0]]
            date = 0
            m = 1   
            for month in l_month :
                if month[:3] == line.split(';')[0].split('/')[0] :
                    date += 100 * m
                m += 1
            date += int(line.split(',')[0].split('/')[2])*10000
            date += int(line.split(',')[0].split('/')[1])
            l_dates.append(date)

l_dates_final = l_dates[1:]

date_to_append = [20120125, 20120425, 20120620, 20120801, 20120913, 20121024, 20121212, 20130130,
20130130, 20130320, 20130501, 20130619, 20130918, 20131030, 20131218, 20140129,
20140129, 20140319, 20140430, 20140618, 20140917, 20141029, 20141217]


for date in date_to_append:
    l_dates_final.append(date)


def from_int_dates(integ):
    string = str(integ)
    new_string = string[0]+ string[1] + string[2] + string[3] + "/" + string[4] + string[5] + "/" + string[6] + string[7]

    return datetime.datetime.strptime(new_string, "%Y/%m/%d") 

l_true_date_final = [from_int_dates(date) for date in l_dates_final]
"""
Load data
"""


df_affirmation = pd.read_csv(project_directory + "csv_files/" + "df_affirmation.csv")

df_nasdaq = pd.read_csv(project_directory + "csv_files/" + "nasdaq-historical-chart.csv", header=9)
df_nasdaq = df_nasdaq.rename({"1971-02-01":"Date", "658.10":"Value", "101.340":"Useless"}, axis="columns")


df_interest_rate = pd.read_csv(project_directory + "csv_files/" + "fed-funds-rate-historical-chart.csv", header=16)
df_interest_rate = df_interest_rate.rename({"1954-07-08":"Date", "1.2500":"Value_interest"}, axis="columns")


"""
Helpfull fonction in order to merge
"""

def match_date_nasdaq(liste_true_date, df):

	liste_str_date = [list(pd.DatetimeIndex(df['Date']).year)[ii]*100 +list(pd.DatetimeIndex(df['Date']).month)[ii] for ii in range(len(list(pd.DatetimeIndex(df['Date']).month)))]
	liste_cut_true_date = [int(str(liste_true_date[ii])[:-2]) for ii in range(len(liste_true_date))]

	liste_nasdaq_rate = list()

	for date in liste_cut_true_date:

		for jj in range(len(liste_str_date)):

			if liste_str_date[jj] == date:
				liste_nasdaq_rate.append(df.Value[jj])

			else:
				pass

	return liste_nasdaq_rate




def match_date_interest(liste_true_date, df):

	liste_str_date = [list(pd.DatetimeIndex(df['Date']).year)[ii]*10000 +list(pd.DatetimeIndex(df['Date']).month)[ii]*100 + list(pd.DatetimeIndex(df['Date']).day)[ii]  for ii in range(len(list(pd.DatetimeIndex(df['Date']).month)))]

	liste_interest_rate = list()

	for date in liste_true_date:

		for jj in range(len(liste_str_date)):

			if liste_str_date[jj] == date:
				liste_interest_rate.append(df.Value_interest[jj])

			else:
				pass


	return liste_interest_rate


liste_nasdaq_rate = match_date_nasdaq(l_dates_final, df_nasdaq)
liste_interest_rate = match_date_interest(l_dates_final, df_interest_rate)


df_affirmation["nasdaq_value"] = liste_nasdaq_rate
df_affirmation["interest_rate"] = liste_interest_rate


df_affirmation.to_csv(project_directory + "csv_files/" + "df_affirmation_finale.csv")







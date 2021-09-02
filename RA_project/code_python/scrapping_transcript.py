import  requests
import pdftotext


project_directory = '/Users/etiennelenaour/Desktop/Stage/code_python/'

l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']

l_dates = list()


#Initialisation de la liste date a l'aide du fichier csv
with open (project_directory+'csv_files/dates_fomc.csv', 'r') as doc :
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

     
date_to_append = [20120125, 20120312, 20120425, 20120620, 20120801, 20120913, 20121024, 20121212,
20130130, 20130320, 20130501, 20130619, 20130918, 20131016, 20131030, 20131218,
20140129, 20140304, 20140319, 20140430, 20140618, 20140630, 20140917, 20141029, 20141217]

for date in date_to_append:
    l_dates.append(date)

#Scrappage des données par date
for date in l_dates:
	
    url = 'https://www.federalreserve.gov/monetarypolicy/files/FOMC'+str(date)+'meeting.pdf'

    r = requests.get(url)
      
    with open(project_directory+'transcript_files_pdf/'+str(date)+'meeting.pdf', "wb") as code:
        code.write(r.content)


    with open(project_directory+'transcript_files_pdf/'+str(date)+'meeting.pdf', 'rb') as entree:
    	pdf = pdftotext.PDF(entree)
    	
    with open(project_directory+'transcript_files_text/'+str(date)+'meeting.txt', 'w') as sortie:
    	sortie.write("\n\n".join(pdf))
    	sortie.close

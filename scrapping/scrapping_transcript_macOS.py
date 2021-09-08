#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 21:26:45 2021

@author: Claire He
Transcripts scrapping that works also on MacOS and Linux distributions. 
"""

import  requests
from PyPDF2 import PdfFileReader
#from PyPDF2 import PdfFileWriter 
import os
from tqdm import trange
dir_name = os.path.dirname(__file__)
project_directory = dir_name



l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']

def scrapping_transcript(date_to_append):
    l_dates = list()
    
    problem_date = []
    for date in date_to_append:
        l_dates.append(date)
    #Scrappage des données par date
    for date in l_dates:
    	
        url = 'https://www.federalreserve.gov/monetarypolicy/files/FOMC'+str(date)+'meeting.pdf'
    
        r = requests.get(url)
        with open(project_directory+'/transcript_files_pdf/'+str(date)+'meeting.pdf', "wb") as code:
            code.write(r.content)
            
        pdf_file = open(project_directory+'/transcript_files_pdf/'+str(date)+'meeting.pdf', 'rb')
        try :
            pdfReader = PdfFileReader(pdf_file)
            count = pdfReader.numPages
            output = []
            for i in trange(count):
                page = pdfReader.getPage(i)
                output += page.extractText()
            
            txtfile = open(project_directory+'/transcript_files_txt/'+str(date)+"meeting.txt","a")
            txtfile.writelines(output)
        except:
            problem_date.append(date)
    
    
    # Storing problematic dates
    
    txtfile = open(project_directory+'/transcript_files_txt/problematic_dates.txt', 'a')
    for elem in problem_date:
        txtfile.writelines("\n"+elem)
    
    # Storing non problematic dates
    
    txtfile = open(project_directory+'/transcript_files_txt/scrapped_dates.txt', 'a')
    date_new=[]
    for elem in l_dates:
        if elem not in problem_date:
            date_new.append(elem)
            txtfile.writelines("\n"+elem)
    
    return date_new

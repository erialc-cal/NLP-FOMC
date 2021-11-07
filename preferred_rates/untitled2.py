#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 22:48:18 2021

@author: Claire He 

One thing you can do (in the meanwhile, before we get more into the LDA) is to see if it is doable to put in an excel or txt file the desired fund rates of FOMC members from the 70s to 1996.  There is a book (attached) that reports the preferred rates of each committee members (according to their interpretation of the members' speeches)

1) The idea is to create a file with 4 columns (see screenshot uno.png)
2) First column is the member number (see file with numbers associated to the names)
3) Second column is the meeting number (see file as well)
4) Third column is the desired rate for all the members (the voting members and those who do not vote, called the "alternates".
5)  The 5th column is the bias.   After the desired fund, there are some letters BS, BE, A, etc.  This is the so-called " bias" of a member  (the bias is intended to give an indication of likely future policy moves: for instance, BE means that in the future the member expected "easing" of interest rate, BS meant that the bias was symmetric (neither easing or tightening). 

The book gives more information (summary statistics), which we do not need. 


"""

from PyPDF2 import PdfFileReader
#from PyPDF2 import PdfFileWriter 
import os
from tqdm import trange
dir_name = os.path.dirname(__file__)
project_directory = dir_name
#%%

def pdf_to_txt(file):

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


#%% 

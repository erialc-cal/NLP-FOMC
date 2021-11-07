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
pdf_file = open(project_directory+'/committee_decisions.pdf', 'rb')


#%% USING PYPDF2 ----- PREFER USING PDFMINER AS SPACES ARE NOT TAKEN IN ACCOUNT IN THIS METHOD

def pdf_to_txt(file):
    """ from pdf with file as path creates text document """
    try :
        pdfReader = PdfFileReader(file)
    except:
        pass
    count = pdfReader.numPages
    output = []
    for i in trange(count):
        page = pdfReader.getPage(i)
        output += page.extractText().split()
        
            
    txtfile = open(project_directory+'/committee_decisions.txt',"a")
    txtfile.writelines(output)    
    return output

#%% USING PDFMINER 

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def convert_pdf_to_string(file_path):

	output_string = StringIO()
	with open(file_path, 'rb') as in_file:
	    parser = PDFParser(in_file)
	    doc = PDFDocument(parser)
	    rsrcmgr = PDFResourceManager()
	    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	    interpreter = PDFPageInterpreter(rsrcmgr, device)
	    for page in PDFPage.create_pages(doc):
	        interpreter.process_page(page)

	return(output_string.getvalue())

txt = convert_pdf_to_string(project_directory+'/committee_decisions.pdf')

            
txtfile = open(project_directory+'/committee_decisions_raw.txt',"a")
txtfile.writelines(txt)  
#%%


#%% 

string_start = "Individual voters desired funds rates" # Individual alternates desired funds rates
string_stop = "Summary statistics"
#ss1 = len(string_start.split())


import nltk
nltk.data.path.append('nltk_data')
from nltk.tokenize import word_tokenize
import re 
split_text = list(filter(None, txt.split('\n')))
split_text = [re.sub(r'[^\w\s]', '', elem) for elem in split_text]


#%% # GET MEETING DATE 
months = ['January', 'February', 'March','April', 'May', 'June', 'July','August','September','October','November', 'December']
def get_dates(text):
    date = []
    for elem in text:
        try:
            if elem.split()[0] in months:
                date.append(' '.join(elem.split()[:3]))
        except:
            pass
    return date

date = get_dates(split_text)

#%% # GET MEETING NAMES 
        
def get_names(text):
    """ get names and add them to the name list starting by the name indexed by idx"""
    name_list= []
    name_list.append(text[2])
    for elem in text[3:]:
        if elem != string_stop:
            name_list.append(elem)
        else :
            break
    return name_list[:-1]

idx=0
names = []
stops = []
while idx < len(split_text): 
    elem = split_text[idx]
    if elem == string_start :
        start = idx
        name_list = get_names(split_text[start:])
     #   rate_list, bias_list = get_numbers(split_text, len(name_list))
         
        idx += len(name_list)+1
        stops.append(len(name_list))
        names.append(name_list)
    else :
        idx+=1

### UNE ERREUR DE SCRAPPING ARRIVE : LORSQUE LE TEXTE EST MAL ALIGNE, UN RATE EST ENREGISTRE 
# AU MILIEU DES NOMS. ON LE RECUPERE CAR C'EST LE PREMIER RATE A LA MAIN POUR FAIRE LA CORRECTION. 
   

 #%%    GET RATES
 
 
def get_numbers(text, stop):
    rate_list=[]
    bias_list= []
    for elem in text:
        if elem == "Median all":
            idx 
            
            
    
    
#%% USING A COMBINATION TO GET EVERY PAGE




def pdf_per_page_to_txt(file_path):
    pdf = PdfFileReader(open(file_path, "rb"))
    fp = open(file_path, 'rb')
    num_of_pages = pdf.getNumPages()
    extract = ""
    for i in trange(num_of_pages):
      inside = [i]
      pagenos=set(inside)
      rsrcmgr = PDFResourceManager()
      retstr = StringIO()
      codec = 'utf-8'
      laparams = LAParams()
      device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
      interpreter = PDFPageInterpreter(rsrcmgr, device)
      password = ""
      maxpages = 0
      caching = True
      text = ""
      for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
        text = retstr.getvalue()
        retstr.truncate(0)
        txtfile = open(project_directory+f'/committee_decisions_{i}.txt',"a")
        txtfile.writelines(text)  


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 11:01:03 2021

@author: Claire He
Main file
"""
import os
dir_name = os.path.dirname(__file__)
print(dir_name)
os.chdir(dir_name)
from update_scrapping import get_date_list
from scrapping_transcript_macOS import scrapping_transcript
from from_transcript_to_text_Claire import convert_transcript_wordset
from transcript_to_dataset import main_dataframe_constructor
import datetime as dt 


scrapping_start_year = 2012

year_l = [str(i) for i in range(scrapping_start_year, dt.datetime.now().year-5)] 
# actualise la liste d'années à partir de scrapping start year

date_list = get_date_list(year_l)


if __name__ == '__main__':
    
    ### SCRAPPING
    try :
        os.mkdir(dir_name+'/transcript_files_pdf/')
        os.mkdir(dir_name+'/transcript_files_txt/')
    except:
        pass
    date_new = scrapping_transcript(date_list) # successful scrapped dates
    
    ### CLEANING
    try :
        os.mkdir(dir_name+'/transcript_to_word_set/')
    except: 
        pass
    convert_transcript_wordset(date_new) # creates wordset
    
    ### CREATING DATASET
    main_dataframe_constructor(date_new)
    
    
    
    
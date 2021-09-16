#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 11:01:03 2021

@author: Claire He
Main file

Le code suivant permet de scrapper tous les transcripts de la FOMC à partir de la date renseignée par 
L'utilisateur dans 'scrapping_start_year', les transcripts étant mis à disposition tous les 5 ans. Il suffit d'exécuter ce code pour avoir :
1. Dans le dossier 'transcript_files_pdf' la version pdf des transcripts (officielle)
2. Dans le dossier 'transcript_files_txt' la version convertie en txt des transcripts
3. Dans le dossier 'transcript_to_word_set' la version "bag of words" des transcripts après nettoyage et lemmatization. 
4. Dans le dossier parent, le dataset mis à jour. 


"""
import os
dir_name = os.path.dirname(os.path.abspath(__file__)) # os.path.dirname(__file__)
os.chdir(dir_name)
from update_scrapping import get_date_list
from scrapping_transcript_macOS import scrapping_transcript
from from_transcript_to_text_Claire import convert_transcript_wordset
from transcript_to_dataset import main_dataframe_constructor2
import datetime as dt 



#######################################################################################
######################### PARTIE A MODIFIER PAR L'UTILISATEUR #########################


scrapping_start_year = 2015



#######################################################################################
######################### PARTIE A MODIFIER PAR L'UTILISATEUR #########################


year_l = [str(i) for i in range(scrapping_start_year, dt.datetime.now().year-5)] 
# actualise la liste d'années à partir de scrapping start year

date_list = get_date_list(year_l)



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
main_dataframe_constructor2(date_new)




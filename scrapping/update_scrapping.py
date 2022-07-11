#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 15:00:41 2021

@author: Claire

Script purpose : to get all the latest published transcripts' dates.
To be used jointly with scrapping_transcript.py
"""

import numpy as np
import pandas as pd
from urllib.request import Request, urlopen
import bs4
import itertools

def get_year_list():
    """
    To get the list of all the years of published transcripts.

    Returns
    -------
    year : list containing years for published transcripts

    """
    url = 'https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm'
	# updated pour contourner les mod_security ajoutés sur le site
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    request_text = urlopen(req).read()
    page = bs4.BeautifulSoup(request_text, "lxml")
    links,year = [],[]
    for link in page.find_all('a'):
        links.append(link.get('href'))
    # Years appear in <a href="/monetarypolicy/fomchistorical2015.htm"> 
    for elem in links :
        if 'fomchistorical' in elem:
            year.append(elem[30:34]) 
    return year

def month_string_to_number(string):
    m = {
        'jan': "01",
        'feb': "02",
        'mar': "03",
        'apr':"04",
         'may':"05",
         'jun':"06",
         'jul':"07",
         'aug':"08",
         'sep':"09",
         'oct':"10",
         'nov':"11",
         'dec':"12"
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

def convert_to_date(date_string):
    date_num = []
    for string in date_string :
        try: 
            if len(string.split())==5 : # format is Month XX-YY Meeting - Year            
                mon, day, _, _, year = string.split()
            
            elif len(string.split())> 5 : # format is Month1 XX-Month2 YY Meeting - Year
                mon = string.split()[1].split('-')[1] 
                _, _, day, _,_,year = string.split()
            
            month_string = month_string_to_number(mon)
        
        # print(day, month_string, year)
        
            if len(day) > 2 : # day format is either "XX-YY" or "X-Y"
                _, nday = day.split("-") # the second day (YY or Y) matches the date
                if len(nday)==1: # if Y, add 0 to string to get 0Y
                    date = year+month_string+"0"+nday 
                else :  
                    date = year+month_string+nday 
            elif len(day)==1: 
                date = year+month_string+"0"+day
            else : 
                date = year+month_string+day
            # ex: January 27-28 2015 -> 20150128
            date_num.append(date)
        except:
            pass
        
    return date_num

def get_date_list(year):
    """
    To get the list of all the dates of published transcripts.

    Parameters
    ----------
    year : list of years of interest.
    Returns
    -------
    date : list of all dates of interest for published transcripts. The format is chosen so scrapping_transcript.py can be used on the output.

    """
    date = []
    for year_date in year:
        url =  'https://www.federalreserve.gov/monetarypolicy/fomchistorical'+year_date+'.htm'
        # Dates appear in the 5th header from https://www.federalreserve.gov/monetarypolicy/fomchistorical{year}.htm
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        request_text = urlopen(req).read()
        page = bs4.BeautifulSoup(request_text, "lxml")
        titles = []
        for title in page.find_all('h5'):
            titles.append(title.text)
        # <h5 class="panel-heading panel-heading--shaded">January 27-28 Meeting - 2015</h5> 
        
        date.append(convert_to_date(titles))
    return list(itertools.chain(*date))
        
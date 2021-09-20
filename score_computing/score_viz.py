#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 16:03:17 2021

@author: Claire He

Plotting scores and visuals
This file is a script not a module. 
"""
#%% Packages 
import numpy as np
import os 
project_directory = os.path.dirname(__file__)
parent, _ = os.path.split(project_directory)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime as dt

#%% Data

df = pd.read_csv(parent+'/updated_version_6.csv', low_memory=True)
df.Date = df.Date.astype('datetime64')

#%% Global visuals

def plot_mean_scores_by_yearspan(df, start_year, end_year):
    plt.figure()
    mask = (df.Date.dt.year >= start_year) & (df.Date.dt.year <= end_year)
    df = df[mask]
    x = ['econo', 'academ', 'uncertainty', 'hostility', 'positivity', 'affirmation', 'virtue', 'vice']
    y = [np.mean(df.score_econo), np.mean(df.score_academ), np.mean(df.score_uncert), np.mean(df.score_hostile),np.mean(df.score_posi), np.mean(df.score_affi), np.mean(df.score_virtue), np.mean(df.score_vice)]
    sns.barplot(x,y)
    plt.title(f"Mean value of all scores on statements made in from {np.min(df.Date)} to {np.max(df.Date)}")
    
plot_mean_scores_by_yearspan(df, 1976, 2014)
plot_mean_scores_by_yearspan(df, 2015, 2015)

#%% Per chair visuals

######################################################################################

def plot_score_hawkish(df):
    
    sns.relplot(x='Date', y='score_hawkish', hue='chair_in_charge', data=df)
    plt.xticks(df.Date.dt.year,range(len(pd.unique(df.Date.dt.year))), rotation=90)
    plt.ylabel("Difference Hawkish Score")
    plt.title("Difference Hawkish Score by meeting (chair score - total score)")
    plt.show()
    plt.close()

######################################################################################

def plot_score_positivity_chair(df):
    plt.figure()
    sns.relplot(x='Date', y='score_posi', hue='chair_in_charge', data=df)
    plt.xticks(df.Date.dt.year,range(len(pd.unique(df.Date.dt.year))), rotation=90)
    plt.ylabel("Positivity Chair")
    plt.title("Positivity Chair by meeting")
    plt.show()
    plt.close()


def plot_score_positivity_total(df):
    plt.figure()
    sns.relplot(x='Date', y='score_posi', hue='chair_in_charge', data=df)
    plt.xticks(df.Date.dt.year,range(len(pd.unique(df.Date.dt.year))), rotation=90)
    plt.ylabel("Positivity Total")
    plt.title("Positivity Total by meeting")
    plt.show()
    plt.close()


def plot_score_positivity_difference(df):
    plt.figure()
    sns.relplot(x='Date', y='score_posi', hue='chair_in_charge', data=df)
    plt.xticks(df.Date.dt.year,range(len(pd.unique(df.Date.dt.year))), rotation=90)
    plt.ylabel("Difference Positivity")
    plt.title("Difference Positivity by meeting (chair score - total score)")
    plt.show()
    plt.close()


plot_score_hawkish(df)
plot_score_positivity_chair(df)
plot_score_positivity_difference(df)
plot_score_positivity_total(df)

#%% Per interlocutor visuals
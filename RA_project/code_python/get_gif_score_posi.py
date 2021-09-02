
import glob
from PIL import Image
import pandas as pd


"""
date
"""

project_directory = '/Users/etiennelenaour/Desktop/Stage/'
l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']
l_dates = list()

df = pd.read_excel('/Users/etiennelenaour/Desktop/Stage/csv_files/df_statement_size.xlsx')
liste_date = list(df.Date.unique())





"""
Create gif
"""


# filepaths
filenames = [project_directory + 'image_tempo/' + 'chair_tempo_' + str(date)[:10] + '.png' for date in liste_date[100:]]
fp_out = project_directory + '/movie_tempo.gif'

#
img, *imgs = [Image.open(f) for f in filenames]
img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=900, loop=0)









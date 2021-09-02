import ast
import json





"""
Main
"""

project_directory = '/Users/etiennelenaour/Desktop/Stage/'
l_month = ['January','February','March','April','May','June','July','August','September','October','November','December']
l_dates = list()


with open(project_directory+'dico_person/'+'dico_person.txt', 'w') as doc:
	doc.readlines()   



dictionary = ast.literal_eval(content)
print(dictionary.keys())

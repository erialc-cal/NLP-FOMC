project_directory = '/Users/etiennelenaour/Desktop/text_file/'
project_directory_output = '/Users/etiennelenaour/Desktop/Stage/'



def debut_statement(liste):

	sentence_idx = 0
	condition = True
	while condition:

		if ("CHAIRMAN" in liste[sentence_idx]) or ("CHAIR" in liste[sentence_idx]):
			print(liste[sentence_idx])
			condition = False

			return sentence_idx

		else:
			sentence_idx += 1 






date_to_append = [20120125, 20120425, 20120620, 20120801, 20120913, 20121024, 20121212, 20130130,
20130130, 20130320, 20130501, 20130619, 20130918, 20131030, 20131218, 20140129,
20140129, 20140319, 20140430, 20140618, 20140917, 20141029, 20141217]


for date in date_to_append:

	with open(project_directory+str(date)+'meeting.txt', 'r') as doc:
		content = doc.readlines()
		output = content[debut_statement(content):]

	with open(project_directory_output + 'transcript_short_version_txt_second/' + str(date) + 'clean_meeting.txt', 'w') as sortie:
		sortie.write(str(output))



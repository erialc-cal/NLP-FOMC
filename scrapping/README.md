# FOMC transcripts - scrapping



Le dossier permet de scrapper tous les transcripts de la FOMC à partir de la date renseignée par l'utilisateur, les transcripts étant mis à disposition tous les 5 ans. 
Il suffit d'exécuter le code de `__main__.py` pour avoir :
1. Dans le dossier 'transcript_files_pdf' la version pdf des transcripts (officielle)
2. Dans le dossier 'transcript_files_txt' la version convertie en txt des transcripts
3. Dans le dossier 'transcript_to_word_set' la version "bag of words" des transcripts après nettoyage et lemmatization. 
4. Dans le dossier parent, le dataset mis à jour. 

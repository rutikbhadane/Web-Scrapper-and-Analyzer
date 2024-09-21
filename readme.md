# to run this script 
# first of all activate the virtual environment file .venv
# using activate  command
# then run this below command 
# pip install -r requirements.txt

# to scrap articles from the input file 
## execute the scrap.py file 
# the articles are scrapped using bs4 and requests 
# to analyse the scrapped articles using nltk 
## execute the main.py file 

# explaination of main.py file
## the scrapped articles are stored in the articles folder, 
# the main.py script collects all the possible stopwords , positive words and negative words from the master dictionary using the nltk library
## the articles are analysed using re library for better analysis
# os library is used for file handling and manipulation 


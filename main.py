# this code is successful and works well
# this script analyzes the articles scrapped and prepares full report and stores it in output excel file
import os
import re
import nltk
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Downloading nltk resources such as stopwords and punkt
nltk.download('punkt')
nltk.download('stopwords')

# Loading english language stop words from the NLTK library
stop_words = set(stopwords.words('english'))

# Load stop words from files
def load_stop_words(stopwords_folder):
    custom_stop_words = set()
    for filename in os.listdir(stopwords_folder):
        filepath = os.path.join(stopwords_folder, filename)
        with open(filepath, 'r',errors="ignore") as file:
            for line in file:
                custom_stop_words.add(line.strip().lower())
    return stop_words.union(custom_stop_words)

# Load positive and negative words from MasterDictionary
def load_dictionary(dictionary_folder, stop_words):
    positive_words = set()
    negative_words = set()
    
    with open(os.path.join(dictionary_folder, 'positive-words.txt'), 'r') as file:
        for line in file:
            word = line.strip().lower()
            if word and word not in stop_words:
                positive_words.add(word)
                
    with open(os.path.join(dictionary_folder, 'negative-words.txt'), 'r') as file:
        for line in file:
            word = line.strip().lower()
            if word and word not in stop_words:
                negative_words.add(word)
                
    return positive_words, negative_words

# Clean and tokenize text
def clean_and_tokenize(text, stop_words):
    tokens = word_tokenize(text)
    cleaned_tokens = [token.lower() for token in tokens if token.lower() not in stop_words and token.isalpha()]
    return cleaned_tokens

# Calculate sentiment scores
def calculate_scores(tokens, positive_words, negative_words):
    positive_score = sum(1 for word in tokens if word in positive_words)
    negative_score = sum(1 for word in tokens if word in negative_words)
    total_words = len(tokens)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)
    
    return positive_score, negative_score, polarity_score, subjectivity_score

# Calculate readability scores
def calculate_readability(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word for word in words if word.isalpha()]
    num_sentences = len(sentences)
    num_words = len(words)
    
    # Average Sentence Length
    avg_sentence_length = num_words / num_sentences if num_sentences else 0
    
    # Count complex words (words with more than two syllables)
    complex_words = [word for word in words if count_syllables(word) > 2]
    percentage_complex_words = len(complex_words) / num_words if num_words else 0
    
    # Gunning Fog Index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    return avg_sentence_length, percentage_complex_words, fog_index

# Calculate average number of words per sentence
def average_words_per_sentence(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word for word in words if word.isalpha()]
    num_sentences = len(sentences)
    num_words = len(words)
    
    avg_words_sentence = num_words / num_sentences if num_sentences else 0
    return avg_words_sentence

# Count complex words
def count_complex_words(words):
    return sum(1 for word in words if count_syllables(word) > 2)

# Count syllables in a word
def count_syllables(word):
    word = word.lower()
    syllable_count = len(re.findall(r'[aeiouy]+', word))
    if word.endswith(('es', 'ed')) and not word.endswith(('le')):
        syllable_count -= 1
    return syllable_count if syllable_count > 0 else 1

# Count personal pronouns
def count_personal_pronouns(text):
    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
    return len(pronouns)

# Calculate average word length
def average_word_length(words):
    total_length = sum(len(word) for word in words)
    avg_word_length = total_length / len(words) if words else 0
    return avg_word_length

# Process a single text file and return the results as a dictionary
# this function processes single text file and returns all the analysis 
def process_single_file(file_path, stop_words, positive_words, negative_words):
    with open(file_path, 'r',errors="ignore") as file:
        text = file.read()
    
    # Clean and tokenize the text
    cleaned_tokens = clean_and_tokenize(text, stop_words)
    cleaned_text = ' '.join(cleaned_tokens)
    
    # Calculate sentiment scores
    positive_score, negative_score, polarity_score, subjectivity_score = calculate_scores(cleaned_tokens, positive_words, negative_words)
    
    # Calculate readability scores
    avg_sentence_length, percentage_complex_words, fog_index = calculate_readability(text)
    
    # Calculate average number of words per sentence
    avg_words_sentence = average_words_per_sentence(text)
    
    # Count complex words
    num_complex_words = count_complex_words(cleaned_tokens)
    
    # Count total words after cleaning
    total_cleaned_words = len(cleaned_tokens)
    
    # Calculate syllable count per word
    syllable_counts = [count_syllables(word) for word in cleaned_tokens]
    avg_syllables_per_word = sum(syllable_counts) / len(syllable_counts) if syllable_counts else 0
    
    # Count personal pronouns
    num_personal_pronouns = count_personal_pronouns(text)
    
    # Calculate average word length
    avg_word_length = average_word_length(cleaned_tokens)
    
    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_words_sentence,
        'COMPLEX WORD COUNT': num_complex_words,
        'WORD COUNT': total_cleaned_words,
        'SYLLABLE PER WORD': avg_syllables_per_word,
        'PERSONAL PRONOUNS': num_personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }

# Process all files in a folder and merge results with an existing Excel file
def process_all_files(folder_path, stopwords_folder, dictionary_folder, output_excel_path):
    # Load stop words and dictionaries
    stop_words = load_stop_words(stopwords_folder)
    positive_words, negative_words = load_dictionary(dictionary_folder, stop_words)
    
    # Read the existing Excel file
    df_existing = pd.read_excel(output_excel_path)
    
    # Prepare a DataFrame to store new results
    results = []
    
    # Process each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            url_id = filename.split('.')[0]
            result = process_single_file(file_path, stop_words, positive_words, negative_words)
            result['URL_ID'] = url_id
            results.append(result)
    
    input_file = '#MENTION YOUR OWN INPUT FILE'
    df_inp = pd.read_excel(input_file)
    # using input file to merge 
    for index, row in df_inp.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
    # Create a DataFrame from the new results
    df_new = pd.DataFrame(results)
    
    # Merge the new results with the existing DataFrame based on URL_ID
    df_combined = pd.merge(df_inp, df_new, on='URL_ID', how='left')
    # with basic changes in the code you can use it for your own use
    # Write the updated DataFrame back to the Excel file
    df_combined.to_excel(output_excel_path,index=False,engine='openpyxl')
    #df_combined.to_excel(output_excel_path, index=False)

# Paths to directories and output file
folder_path = 'articles'
stopwords_folder = 'StopWords'
dictionary_folder = 'MasterDictionary'
output_excel_path = 'Output Data Structure.xlsx'

# Process all files and write to Excel
process_all_files(folder_path, stopwords_folder, dictionary_folder, output_excel_path)

# Web Scraper and Analyzer

## Overview
This project is a web scraper built in Python that reads articles from specified URLs in an input Excel file, analyzes them, and writes the results back into the same file. The output includes various metrics for each article, providing insights into its content.

## Features
- Reads URLs from an Excel file.
- Scrapes articles and analyzes them for:
  - Sentiment Scores (Positive, Negative, Polarity, and Subjectivity)
  - Readability Scores (Average Sentence Length, Percentage of Complex Words, FOG Index)
  - Counts (Complex Words, Total Words, Personal Pronouns)
  - Average Word Length and Syllable Count
- Outputs detailed metrics for each article in the specified output format.

## Requirements
- Python 3.x
- Required libraries (install via `requirements.txt`)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
2. # Web Scraper Project

## Overview
This project is a web scraper built in Python that reads articles from specified URLs in an input Excel file, analyzes them, and writes the results back into the same file. The output includes various metrics for each article, providing insights into its content.

## Features
- Reads URLs from an Excel file.
- Scrapes articles and analyzes them for:
  - Sentiment Scores (Positive, Negative, Polarity, and Subjectivity)
  - Readability Scores (Average Sentence Length, Percentage of Complex Words, FOG Index)
  - Counts (Complex Words, Total Words, Personal Pronouns)
  - Average Word Length and Syllable Count
- Outputs detailed metrics for each article in the specified output format.

## Requirements
- Python 3.x
- Required libraries (install via `requirements.txt`)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. **Install required libraries:**

```bash
pip install -r requirements.txt
```
4. **Download NLTK resources:**
    The script requires certain NLTK resources. Make sure to run the following in a Python shell or add it to the script:
   
```pytho
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```
**Usage**
Prepare an input Excel file with the required URLs. The file should have columns labeled URL_ID and URL.
Run the scraper:
```bash
python main.py
```
The output will be written back to the specified Excel file, Output Data Structure.xlsx.
Output Format
The output file will have the following columns:

[URL_ID, URL, POSITIVE SCORE, NEGATIVE SCORE, POLARITY SCORE, SUBJECTIVITY SCORE, AVG SENTENCE LENGTH, PERCENTAGE OF COMPLEX WORDS, FOG INDEX, AVG NUMBER OF WORDS PER SENTENCE, COMPLEX WORD COUNT, WORD COUNT, SYLLABLE PER WORD, PERSONAL PRONOUNS, AVG WORD LENGTH]

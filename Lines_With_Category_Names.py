import gzip
import json
import re


file = 'enwiki-country.json.gz'

def extract_uk_article(file):
    with gzip.open(file, 'rt', encoding='utf-8') as file:
        for line in file:
            # Parse the JSON line
            article = json.loads(line)
            # Check if the title is "United Kingdom"
            if article['title'] == 'United Kingdom':
                return article['text']

def extract_category_lines(text):
    category_pattern = re.compile(r'\[\[Category:.*?\]\]')
    category_lines = category_pattern.findall(text)
    return category_lines

uk_article_body = extract_uk_article(file)

category_lines = extract_category_lines(uk_article_body)


for line in category_lines:
    print(line)

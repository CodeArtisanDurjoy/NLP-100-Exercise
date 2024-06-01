import gzip
import json

file = 'enwiki-country.json.gz'

def extract_uk_article(file):
    with gzip.open(file, 'rt', encoding='utf-8') as file:
        for line in file:
            # Parse the JSON line
            article = json.loads(line)
            # Check if the title is "United Kingdom"
            if article['title'] == 'United Kingdom':
                return article['text']


uk_article_body = extract_uk_article(file)

print(uk_article_body)

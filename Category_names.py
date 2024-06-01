import gzip
import json
import re


path = 'enwiki-country.json.gz'

def extract_uk_article(path):
    with gzip.open(path, 'rt', encoding='utf-8') as file:
        for line in file:
            article = json.loads(line)
            if article['title'] == 'United Kingdom':
                return article['text']

def extract_category_lines(text):
    category_pattern = re.compile(r'\[\[Category:.*?\]\]')
    category_lines = category_pattern.findall(text)
    return category_lines

def extract_category_names(category_lines):
    category_names = []
    for line in category_lines:
        # Extract the category name
        match = re.search(r'\[\[Category:(.*?)(\|.*)?\]\]', line)
        if match:
            category_names.append(match.group(1))
    return category_names

uk_article_body = extract_uk_article(path)

category_lines = extract_category_lines(uk_article_body)

category_names = extract_category_names(category_lines)

for name in category_names:
    print(name)

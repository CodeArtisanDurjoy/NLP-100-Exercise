import gzip
import json
import re


path = 'enwiki-country.json.gz'

def extract_uk_article(path):
    with gzip.open(path, 'rt', encoding='utf-8') as file:
        for line in file:
            # Parse the JSON line
            article = json.loads(line)
            # Check if the title is "United Kingdom"
            if article['title'] == 'United Kingdom':
                return article['text']

def extract_section_names(text):
    section_pattern = re.compile(r'^(=+)\s*(.*?)\s*\1$', re.MULTILINE)
    sections = section_pattern.findall(text)
    section_list = [(len(equal_signs) - 1, section_name) for equal_signs, section_name in sections]
    return section_list

uk_article_body = extract_uk_article(path)

sections = extract_section_names(uk_article_body)

for level, name in sections:
    print(f'Level {level}: {name}')

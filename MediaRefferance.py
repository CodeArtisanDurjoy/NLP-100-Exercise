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

def extract_media_references(text):
    # Regular expression to match media file references
    media_pattern = re.compile(r'\[\[(File|Image):.*?\]\]')
    # Find all media references
    media_references = media_pattern.findall(text)
    return media_references

uk_article_body = extract_uk_article(path)

media_references = extract_media_references(uk_article_body)


for reference in media_references:
    print(reference)

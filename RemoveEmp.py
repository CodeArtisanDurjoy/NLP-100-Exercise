import gzip
import json
import re


file_path = 'enwiki-country.json.gz'

def extract_uk_article(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            # Parse the JSON line
            article = json.loads(line)
            # Check if the title is "United Kingdom"
            if article['title'] == 'United Kingdom':
                return article['text']

def extract_infobox(text):
    # Regular expression to match the Infobox country template
    infobox_pattern = re.compile(r'\{\{Infobox country(.*?)\n\}\}', re.DOTALL)
    match = infobox_pattern.search(text)
    if match:
        return match.group(1)
    return None

def remove_emphasis_markup(text):
    # Remove bold markup
    text = re.sub(r"'''(.*?)'''", r'\1', text)
    # Remove italic markup
    text = re.sub(r"''(.*?)''", r'\1', text)
    return text

def parse_infobox(infobox_text):
    infobox_dict = {}
    # Regular expression to match each field in the Infobox
    field_pattern = re.compile(r'\|\s*(.*?)\s*=\s*(.*?)\s*(?=\n\||\n\}\})', re.DOTALL)
    fields = field_pattern.findall(infobox_text)
    for field_name, value in fields:
        clean_value = remove_emphasis_markup(value.strip())
        infobox_dict[field_name.strip()] = clean_value
    return infobox_dict

uk_article_body = extract_uk_article(file_path)

infobox_text = extract_infobox(uk_article_body)


infobox_dict = parse_infobox(infobox_text) if infobox_text else {}


for field, value in infobox_dict.items():
    print(f'{field}: {value}')

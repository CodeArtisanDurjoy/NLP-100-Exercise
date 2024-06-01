import gzip
import json
import re
import requests


source = 'enwiki-country.json.gz'

def extract_uk_article(source):
    with gzip.open(source, 'rt', encoding='utf-8') as file:
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

def remove_internal_links(text):
    # Remove internal links but keep the display text
    text = re.sub(r'\[\[([^|\]]*?\|)?(.*?)\]\]', r'\2', text)
    return text

def remove_mediawiki_markup(text):
    # Remove references
    text = re.sub(r'<ref.*?>.*?</ref>', '', text, flags=re.DOTALL)
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # Remove templates
    text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)
    # Remove any remaining HTML tags
    text = re.sub(r'<.*?>', '', text, flags=re.DOTALL)
    return text

def parse_infobox(infobox_text):
    infobox_dict = {}
    # Regular expression to match each field in the Infobox
    field_pattern = re.compile(r'\|\s*(.*?)\s*=\s*(.*?)\s*(?=\n\||\n\}\})', re.DOTALL)
    fields = field_pattern.findall(infobox_text)
    for field_name, value in fields:
        clean_value = remove_mediawiki_markup(remove_internal_links(remove_emphasis_markup(value.strip())))
        infobox_dict[field_name.strip()] = clean_value
    return infobox_dict

def get_image_url(image_name):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'titles': 'File:' + image_name,
        'prop': 'imageinfo',
        'iiprop': 'url',
        'format': 'json'
    }
    response = requests.get(url, params=params).json()
    pages = response['query']['pages']
    for page_id in pages:
        if 'imageinfo' in pages[page_id]:
            return pages[page_id]['imageinfo'][0]['url']
    return None

# Get the body of the article about the United Kingdom
uk_article_body = extract_uk_article(source)

# Extract the Infobox country
infobox_text = extract_infobox(uk_article_body)

# Parse the Infobox into a dictionary
infobox_dict = parse_infobox(infobox_text) if infobox_text else {}


for field, value in infobox_dict.items():
    print(f'{field}: {value}')

flag_image_name = infobox_dict.get('flag', None)
if not flag_image_name:
    flag_image_name = infobox_dict.get('image_flag', None)


if flag_image_name:
    flag_image_url = get_image_url(flag_image_name)
    print(f'Flag URL: {flag_image_url}')
else:
    print('Flag image not found.')

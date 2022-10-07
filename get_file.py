from bs4 import BeautifulSoup
from bs4.element import Comment
import regex as re
import urllib
import requests
import pandas as pd
CHARS_TO_REPLACE = '.,'

def tag_visible(element):
    """
    """

    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    elif re.match(r"[\s\r\n]+", str(element)):
        return False
    return True

def text_from_html(body):
    """
    This Function takes the body of a text taken from an url source to transform and return it
    as a list containing all the html and text commands written in the URL.
    """

    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)



def count_number_of_mentions(url, word_to_count):
    """
    This function takes a URL and a word and outputs the number of times
    such a word can be found in the URL.
    """

    nbr_of_mentions = 0
    html = requests.get(url).content
    text = text_from_html(html)

    for char in CHARS_TO_REPLACE:
        text = text.replace(char, ' ')

    list_text = text.split()

    for word in list_text:
        if word_to_count.lower() == word.lower():
            nbr_of_mentions += 1

    return nbr_of_mentions


def text_to_file(file_path, url):
    """
    This function takes a URL from which we will extract data. It extracts the text
    from the URL (Web page) file_path where the text
    will be stored locally in the computer
    """

    html = urllib.request.urlopen(url).read()
    text = text_from_html(html)
    text_file = open(file_path, 'w', encoding='utf-8')

    list_text = text.split()

    i = 0
    for word in list_text:
        if i == 10:
            text_file.write(word + '\n')
            i = 0
        else:
            text_file.write(word + ' ')
            i += 1

    text_file.close()

def replace(text):
    """
    This function takes
    :param text:
    :return:
    """

    for char in CHARS_TO_REPLACE:
        text = text.replace(char, ' ')

    return text

def txt_file_to_list(txt_file):
    with open(txt_file) as f:
        lines = f.readlines()
        list_url = [url.replace('\n', '') for url in lines]

    return list_url

def create_df_url(txt_file):
    list_url = txt_file_to_list(txt_file)
    df = pd.DataFrame([1,1,1,1,1,1,1])
    return df

def get_data(txt_file, word):
    list = [count_number_of_mentions(url, word) for url in txt_file_to_list(txt_file)]
    return list, word

def add_data_df(df, data, name_column):
    df = df.assign(Coucou=data)
    return df

txt_file = 'list_url.txt'
word = 'PCQ'
df = create_df_url(txt_file)
data = get_data(txt_file, word)[0]
add_data_df(df, data, word)
print(df)

#list = [count_number_of_mentions(url, 'PCQ') for url in txt_file_to_list(txt_file)]
#print(list)


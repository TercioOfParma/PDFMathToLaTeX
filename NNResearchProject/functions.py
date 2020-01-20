import re
import wikipedia as wiki
from unidecode import unidecode
import config


def generate_dictionary(tag, max_word_length):
    print(tag)
    lst = []
    if "mt" in tag:
        print("true")
        wiki.set_lang("en")
    else:
        wiki.set_lang(tag)
    for topic in config.language_tags[tag]:
        print(topic + " " +  tag)
        page = wiki.WikipediaPage(topic)
        content = page.content
        content = unidecode(content)
        lst = lst + process(content, max_word_length, tag)
        #print(lst)

    return lst

def process(page_content, max_word_length, tag):
    words = re.sub(r'[^a-zA-Z ]', '', page_content)
    #print(tag)
    if "mt" in tag:
        words = re.sub(r'[a-zA-Z]', '', page_content)
        words = re.sub(r'[,\."\'\t\n\r]', '', words)
        #print(words)    
    #print("Word List 1: " + lower)
    word_list = words.split()
    #print(word_list)
    short_words = []
    for word in word_list:
        #print(word)
        if len(word) <= max_word_length:
            short_words.append(word)
            #print(len(short_words))
    #print(short_words)
    return short_words

def convert_dic_to_vector(dic, max_word_length):
    new_list = []
    for word in dic:
        #print(word)
        vec = ''
        n = len(word)
        for i in range(n):
            current_letter = word[i]
            ind = ord(current_letter)
            placeholder = (str(0)*ind) + str(1) + str(0)*(127-ind)
            vec = vec + placeholder
        if n < max_word_length:
            excess = max_word_length-n
            vec = vec +str(0)*128*excess
        new_list.append(vec)
    print(len(new_list))
    return new_list

def create_output_vector(tag_index, number_of_languages):
    out = str(0)*tag_index + str(1) + str(0)*(number_of_languages-1-tag_index)
    return out

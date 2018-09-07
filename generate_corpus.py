# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 19:23:21 2018

@author: Di Yi
"""

from bs4 import BeautifulSoup
import re, os, codecs
from glob import glob


def hasNumber(inputString):
    return any(char.isdigit() for char in inputString)


def process_word(word):
    if hasNumber(word):
        if word[:1] == '.' or word[:1] == ',':
            word = word[1:]
        if word[-1:] == '.' or word[-1:] == ',':
            word = word[:-1]
        return word
    else:
        word = re.sub(r"[^A-Za-z-]+", '', word)
        if word[:1] == '-':
            word = word[1:]
        if word[-1:] == '-':
            word = word[:-1]
        return word


def process_file(file_name, case_folding=True, punctuation=True):
    file1 = codecs.open(file_name, encoding='utf-8')

    if case_folding:  # Perform case_folding
        data = file1.read().lower()
    else:  # Not to perform case_folding
        data = file1.read()

    soup = BeautifulSoup(data, 'html.parser')
    soup.prettify().encode("utf-8")
    soup.find("pre").contents[0]
    data = soup.get_text()
    full_text = []
    if punctuation:  # Perform punctuation
        pattern = re.compile('[\'_!@\s#$%=+~()}{\][^?&*:;\\/|<>"]')
        full_text = pattern.sub(" ", data).split()
        full_text = [e for e in full_text if e not in (',', '.', '-')]
        result_text = []
        for word in full_text:
            if process_word(word) != '':
                result_text.append(process_word(word))
    else:  # Not to perform punctuation
        result_text = full_text.split()
    result_text = remove_tail_nums(result_text)
    return result_text, file_name


def remove_tail_nums(text):
    index = len(text) - 1
    while index > 0:
        try:
            int(text[index])
            index -= 1
        except ValueError:
            break
    return text[:index + 1]


def write_file(text, file_name):
    file1 = open("corpus_without_number/" + file_name[5:-5] + '.txt', 'w')
    file1.truncate()
    for each in text:
        file1.write(each + ' ')
    file1.close()


def write_files(case_folding=True, punctuation=True):
    file_names = glob(os.path.join('cacm', '*.html'))
    for each in file_names:
        text, file_name = process_file(each, case_folding, punctuation)
        write_file(text, file_name)


def main(case_folding=True, punctuation=True):
    write_files(case_folding, punctuation)


main()


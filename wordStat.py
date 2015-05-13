from lxml import html
from lxml.html.clean import Cleaner
from lxml import etree
from collections import Counter
from pprint import pprint

import os
import Frequency
import json
import string
import re
import tokenize


def count_terms(terms):
    global cnt
    for term in terms:
        cnt[term] += 1


def compute_word_frequencies(words):
    """
    :param words: list of strings
    :return: uses the counter object to count the number of occurrences of each string and sorts them by frequency and
    alphabetically and returns them as Frequency objects in a list
    """

    # Cnt should be the list of words
    cnt = []
    count = [i for i in cnt.items()]
    result = [Frequency(i[0], i[1]) for i in sorted(count, key = lambda word: (-word[1], word[0]))]
    return result


def tokenize_string(text):
    '''
    :param text: text to parse
    :return: list of tokens
    '''
    global stopwords
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    words = text.strip().lower().translate(remove_punctuation_map)
    words = [word for word in words.split() if word not in stopwords]
    return words


def remove_stopwords(text):
    '''
    :param text:
    :return:
    '''
    return


def assign_termid(terms):
    """
    :param terms: list of terms from HTML page to assign id
    :return: void
    """
    global term_to_termid, termId
    for i in list(enumerate(terms, termId)):
        if i[1] not in term_to_termid:
            term_to_termid[i[1]] = i[0]
    termId = termId + len(terms)


def add_term2docfreq(terms, docid):
    '''
    Map frequency of term to document. Map it back to termId
    :param terms:
    :param docid:
    :return:
    '''
    global termid_to_docfreq, term_to_termid
    term_set = set(terms)
    for term in term_set:
        term_id = term_to_termid[term]
        if term_id not in termid_to_docfreq:
            termid_to_docfreq[term_id] = dict()
        termid_to_docfreq[term_id][docid] = terms.count(term)


def add_term2docid(terms, filename):
    '''
    Add terms from one document to index
    :param terms: list of terms from one document
    :param filename: path to file
    :return: void
    '''
    global termid_to_docs, term_to_termid
    for term in terms:
        term_id = term_to_termid[term]
        if term_id not in termid_to_docs:
            termid_to_docs[term_id] = set([filename[:-4]])
        else:
            termid_to_docs[term_id].add(filename[:-4])


def read_json(fileName):
    '''
    Read JSON data into dictionary
    :param fileName: path of file
    :return: JSON Data
    '''
    with open(fileName) as data_file:
        data = json.load(data_file)
    return data


def read_stopwords(fileName):
    '''
    Read stop words to list
    :param fileName: path of file
    :return: list of stopwords
    '''
    with open(fileName, 'r') as f:
        stopwords = [line.rstrip() for line in f.readlines()]
        return stopwords


def write_index(fileName):
    '''
    Write index file for TermID => DocIDm, Frequency
    :param fileName: path to file
    :return: void
    '''
    with open(fileName, 'w') as f:
        f.write('TermID => DocID, Term Frequency\n')
        json.dump(termid_to_docfreq, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    # Configuration
    cleaner = Cleaner(style=True, links=True, page_structure=True)
    DATA_PATH = 'data/test_dump'
    INDEX_PATH = 'D:\Documents\CS121\Assignment 3\data\index.txt'
    STOPWORD_PATH = 'stopwords.txt'

    # Global variables
    stopwords = read_stopwords(STOPWORD_PATH)
    cnt = Counter()
    termId = 0
    term_to_termid = dict()
    termid_to_docs = dict()
    termid_to_docfreq = dict()

    try:
        print("Building index...")
        for fileName in os.listdir(DATA_PATH):
            if fileName[-3:] == 'txt':
                print("Parsing " + fileName)
                data = read_json(DATA_PATH + "/" + fileName)
                terms = tokenize_string(data['text'])
                print("Counting term frequency")
                count_terms(terms)
                print("Assigning term id")
                assign_termid(terms)
                print("Get term frequencies for " + fileName + "\n")
                add_term2docfreq(terms, fileName[:-4])
    except Exception as e:
        print(e)
    finally:
        write_index(INDEX_PATH)

    # Printing Test Block
    print('Term => TermID')
    print(termId)

    print('\nTermID => DocID, Term Frequency')
    for i in termid_to_docfreq.items():
        print (i)
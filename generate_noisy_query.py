# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:18:41 2018

@author: Yidi
"""
import random
def get_queries():
    file = open('queries.txt', 'r')
    queries = []
    r = 0
    for each in file:
        r += 1 
        if r <=10:
            queries.append(each)
    return queries

def generate_spelling_error_query(terms):
    terms = terms.split()
    terms_len = len(terms)
    if terms_len >=5:
        num = int(terms_len * 0.4)
    else:
        num= int(terms_len * 0.35)
    
    num = random.randint(0,num)
    for i in range(num):
        num_ran = random.randint(0,terms_len-1)
        term = list(terms[num_ran])
        random.shuffle(term)
        terms[num_ran] = "".join(term)
    return terms
    
def generate_spelling_error_queries():
    queries = get_queries()
    error_queries = []
    for each in queries:
        error_queries.append(generate_spelling_error_query(each))
    return error_queries    

def save_error_queries(queries):
    file = open('noisy_queries.txt','w')
    for query in queries:
        for term in query:
            file.write(term+" ")
        file.write('\n')
    
def main():
    error_queries = generate_spelling_error_queries()
    save_error_queries(error_queries)
    
main()
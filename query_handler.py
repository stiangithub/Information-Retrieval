import aspell
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:25:09 2018

@author: Yidi
"""
def get_queries():
    file = open('noisy_queries.txt','r')
    queries = []
    for query in file:
        queries.append(query)
    return queries

def query_handler(query):
    correcter= aspell.Speller('lang','en')
    query = query.split()
    correct_query = []
    for term in query:
        if len(correcter.suggest(term)) == 0: continue
        correct_query.append(correcter.suggest(term)[0].lower())
    return correct_query

def save_corrected_queries(queries):
    file = open('corrected_queries.txt','w')
    for query in queries:
        for term in query:
            file.write(term+" ")
        file.write('\n')
        
def main():
    error_queries = get_queries()
    correct_queries =[]
    for query in error_queries:
        correct_query = query_handler(query)
        correct_queries.append(correct_query)
    save_corrected_queries(correct_queries)
main()
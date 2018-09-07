#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 12:41:15 2018

@author: stian
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 15:14:47 2018

@author: Yidi
"""
import math
from glob import glob
import os,operator
from nltk.tokenize import regexp_tokenize

doc_len = {}
index = {}
sorted_ql ={}
ql_scores = {}
def generate_unigram():
    global index  
    file_names= glob(os.path.join('stem_corpus','*.txt'))
    for doc_id in file_names:
        file1=open(doc_id,'r')
        doc_id=doc_id[:-4]
        text=file1.read()
        text=text.split()
        for term in text:
            if term not in index:
                index[term]={}
                index[term][doc_id]=1

            elif doc_id not in index[term]:
                index[term][doc_id] = 1
                
            else:
                index[term][doc_id] = index[term][doc_id] + 1
        file1.close()
    sorted_index = sorted(index.items(), key=operator.itemgetter(0), reverse = False)
    return sorted_index


#def get_queries():
#    file = open('cacm_stem.query.txt', 'r')
#    queries = [""] * 65
#    isText = False
#    i = 0
#    for line in file:
#        if (len(line)) == 0: continue
#        elif line[0] == '<' or (line[0] == ' ' and len(line) == 1):
#            isText = False
#            continue
#        else:
#            if not isText:
#                isText = True
#                queries[i] = ""
#                queries[i] += line
#                i += 1
#            else:
#                queries[i - 1] += " "
#                queries[i - 1] += line
#    for i in range(len(queries)):
#        query = queries[i].lower()
#        queries[i] = regexp_tokenize(query, pattern='\w+')
#    return queries[:-1]

        
def doc_length():
    global doc_len
    file_names= glob(os.path.join('stem_corpus','*.txt'))
    for doc_id in file_names:
        file1=open(doc_id,'r')
        doc_id=doc_id[:-4]
        text=file1.read()
        text=text.split()
        doc_len[doc_id]= len(text)
        file1.close()

def doc_sum_len():
    sum = 0
    for each in doc_len:
        sum += doc_len[each]
    return sum
       
#def query_likelihood(queries,quey_id):
#    
#    global sorted_ql
#    global ql_scores
#    lmd = 0.35
#    C = doc_sum_len()
#    
#    file_names= glob(os.path.join('corpus','*.txt'))
#
#    for doc_id in file_names:
#        score = 0
#        doc_id=doc_id[7:-4]
#        D = doc_len[doc_id]
#        for i in range(len(queries)):
#            query = queries[i]
#            cq = 0
#            if query not in index:
#                fqd = 0
#                cq = 0
#                score += 0
#            else:
#                fqd = index[query].get(doc_id,0)
#                for doc in index[query]:
#                    cq += index[query][doc]
#                score += math.log((1 - lmd) * (fqd / D) + lmd * cq / C)
#            if i == len(queries)-1:
#                print(score)
#        ql_scores[doc_id] = score
#    sorted_ql = sorted(ql_scores.items(), key=operator.itemgetter(1), reverse = True)
#    return sorted_ql

def query_likelihood(query_terms,quey_id):
    global sorted_ql
    global ql_scores
    file_names= glob(os.path.join('stem_corpus','*.txt'))
    for doc_id in file_names:
        doc_id=doc_id[:-4]
        D = doc_len[doc_id]
        score = ql_score(doc_id,query_terms,D)
        ql_scores[doc_id] = score
    sorted_ql = sorted(ql_scores.items(), key=operator.itemgetter(1), reverse = True)
    return sorted_ql
    
def ql_score(doc_id,query_terms,D):
    lmd = 0.35
    score =0
    C = doc_sum_len()
    for i in range(len(query_terms)):
        term = query_terms[i]
        cq = 0
        if term not in index:
            fqd = 0
            cq = 0
            score += 0
        else:
            fqd = index[term].get(doc_id,0)
            for doc in index[term]:
                cq += index[term][doc]
            inlog = (1 - lmd) * (fqd / D) + lmd * cq / C
            if inlog == 0: print("INlog is 0")
            score += math.log((1 - lmd) * (fqd / D) + lmd * cq / C)
    return score

def write_scores_to_file(scores,query_id):
    file1=open("results/stem_query_likelihood/query_likelihood_query"+str(query_id)+".txt",'w')
    rank = 0
    for each in scores:
        rank +=1
        if rank <=100:
            file1.write((str(query_id)+' '+'Q0'+' '+each[0]+' '+str(rank)+' '+str(each[1])+' '+'QUERY_LIKELIHOOD'+'\n'))
    file1.close()   
     
def main():
    doc_length()
    generate_unigram()
    f = open("cacm_stem.query.txt",'r')
    queries = []
    for i in f.readlines():
        queries.append(i)
    f.close()
    print(len(queries))
    #queries = get_queries()
    query_id = 0
    for query in queries:
        query_id += 1
        ql_scores=query_likelihood(query.split(),query_id)
        write_scores_to_file(ql_scores,query_id)

main()




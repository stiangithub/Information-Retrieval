# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 19:55:48 2018

@author: Di Yi
"""
from math import log10
from nltk.tokenize import regexp_tokenize
import os,operator
from glob import glob
doc_len = {}
tf_idf_scores = {}
index = {}
sorted_tf_idf = {}
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

def doc_length():
    global doc_len
    file_names= glob(os.path.join('stem_corpus','*.txt'))
    for doc_id in file_names:
        file1=open(doc_id,'r')
        doc_id=doc_id[:-4]
        text=file1.read()
        text=text.split()
        doc_len[doc_id]= len(text)
        
#def get_queries():
#    file = open('cacm_stem.query.txt', 'r')
#    queries = [""] * 8
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

        
def generate_tf_idf_scores(queries,index):
    global tf_idf_scores
    global sorted_tf_idf
    file_names= glob(os.path.join('stem_corpus','*.txt'))
    total_num_of_docs = len(file_names)
    for doc_id in file_names:
        doc_id=doc_id[:-4]
        tf_idf = 0
        for query in queries:
            tf = 0
            idf = 0
            if query not in index:
                continue
            else:
                tf = float(index[query].get(doc_id,0))/float(doc_len[doc_id])
                idf = log10(total_num_of_docs/(len(index[query])))
            tf_idf += tf*idf
        tf_idf_scores[doc_id] = tf_idf
    sorted_tf_idf = sorted(tf_idf_scores.items(), key=operator.itemgetter(1), reverse = True)
    return sorted_tf_idf

def save_index(index,file_name):
    file2=open(file_name,'w')
    for term in index:
        file2.write(term[0]+"  ")
        for doc_id in term[1]:
            file2.write('('+doc_id+',,'+str(term[1][doc_id])+') ')
        file2.write("\n")
    file2.close()
    
def write_scores_to_file(tf_idf_scores,query_id):
    file1=open("results/stem_tf_idf/stem_tf_idf_query"+str(query_id)+".txt",'w')
    rank = 0
    for each in tf_idf_scores:
        rank +=1
        if rank <=100:
            file1.write((str(query_id)+' '+'Q0'+' '+each[0]+' '+str(rank)+' '+str(each[1])+' '+'TF_IDF'+'\n'))
    file1.close()
    
def main():
    uni_index = generate_unigram()  #Unigram Task2 and 3
    save_index(uni_index,'unigram_index.txt')
    print('Unigram index completed')
    doc_length()
    f = open("cacm_stem.query.txt",'r')
    queries = []
    for i in f.readlines():
        queries.append(i)
    f.close()
    query_id =0
    for query in queries:
        query_id += 1
        tf_idf_scores = generate_tf_idf_scores(query.split(),index)
        write_scores_to_file(tf_idf_scores,query_id)


main()
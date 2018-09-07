# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 19:55:59 2018

@author: Yidi
"""
from math import log
from nltk.tokenize import regexp_tokenize
from glob import glob
import os, operator

k1 = 1.2
b = 0.75
k2 = 100
index = {}
doc_len = {}


def generate_unigram():
    global index
    file_names = glob(os.path.join('corpus', '*.txt'))
    for doc_id in file_names:
        file1 = open(doc_id, 'r')
        doc_id = doc_id[7:-4]
        text = file1.read()
        text = text.split()
        for term in text:
            if term not in index:
                index[term] = {}
                index[term][doc_id] = 1

            elif doc_id not in index[term]:
                index[term][doc_id] = 1
            else:
                index[term][doc_id] = index[term][doc_id] + 1
        file1.close()
    sorted_index = sorted(index.items(), key=operator.itemgetter(0), reverse=False)
    return sorted_index


def get_queries():
    file = open('noisy_queries.txt', 'r')
    queries = []
    for sent in file.readlines():
        queries.append(sent.split())
    return queries


def doc_length():
    global doc_len
    file_names = glob(os.path.join('corpus', '*.txt'))
    for doc_id in file_names:
        file1 = open(doc_id, 'r')
        doc_id = doc_id[7:-4]
        text = file1.read()
        text = text.split()
        doc_len[doc_id] = len(text)
        file1.close()


def doc_avdl():
    sum = 0
    for each in doc_len:
        sum += doc_len[each]
    return (sum / len(doc_len))


def get_bm25(R, N, dl, avdl, r, n, f, qf):
    K = k1 * ((1 - b) + b * (float(dl) / float(avdl)))
    first = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    second = (k1 + 1) * f / (K + f)
    third = (k2 + 1) * qf / (k2 + qf)
    return first * second * third


def bm25(queries, query_id, avdl):
    doc_bm25 = {}
    R = 0
    r = 0
    qf = 1
    file_names = glob(os.path.join('corpus', '*.txt'))
    N = len(file_names)
    for doc_id in file_names:
        doc_id = doc_id[7:-4]
        dl = doc_len[doc_id]
        bm25 = 0
        for query in queries:
            if query not in index:
                r = 0
                n = 0
                f = 0
            else:
                r = 0
                n = len(index[query])
                f = int(index[query].get(doc_id, 0))
            bm25 += get_bm25(R, N, dl, avdl, r, n, f, qf)
        doc_bm25[doc_id] = bm25
    sorted_bm25 = sorted(doc_bm25.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_bm25


# def get_rel_list(query_id):
#     files= glob(os.path.join('corpus','*.txt'))
#     doc_list = []
#     rel_list = []
#     rels = open('cacm.rel.fullname.txt', 'r')
#     for rel in rels.readlines():
#         rel = rel.split()
#         if int(rel[0]) == query_id:
#             doc_list.append(rel[2])
#         if int(rel[0]) > query_id: break
#     for file in files:
#         doc = file[7:-4]
#         if doc in doc_list: rel_list.append(doc)
#     return rel_list


# def get_ri(doc_list, rel_list):
#     ri = 0
#     for doc in doc_list:
#         if doc in rel_list:
#             ri += 1
#     return ri


def write_scores_to_file(scores, query_id):
    file1 = open("results/bm25_error_query/bm25_query" + str(query_id) + ".txt", 'w')
    rank = 0
    for each in scores:
        rank += 1
        if rank <= 100:
            file1.write((str(query_id) + ' ' + 'Q0' + ' ' + each[0] + ' ' + str(rank) + ' ' + str(
                each[1]) + ' ' + 'BM25' + '\n'))
    file1.close()


def save_queries(queries):
    file_name = "queries.txt"
    open(file_name, 'w').close()
    result_f = open(file_name, 'a')
    for query in queries:
        newLine = ""
        for word in query:
            newLine += word + " "
        result_f.write(newLine + "\n")


def get_full_name_rel():
    file = open('cacm.rel.fullname.txt', "w")
    rels = open('cacm.rel.txt', 'r')
    for rel in rels.readlines():
        rel = rel.split()
        if len(rel[2]) == 9:
            file.write(" ".join(rel) + "\n")
        elif len(rel[2]) == 8:
            tmp = rel[2]
            rel[2] = tmp[0:5] + "0" + tmp[5:]
            file.write(" ".join(rel) + "\n")
        elif len(rel[2]) == 7:
            tmp = rel[2]
            rel[2] = tmp[0:5] + "00" + tmp[5:]
            file.write(" ".join(rel) + "\n")
        else:
            tmp = rel[2]
            rel[2] = tmp[0:5] + "000" + tmp[5:]
            file.write(" ".join(rel) + "\n")


def main():
    get_full_name_rel()
    doc_length()
    generate_unigram()
    queries = get_queries()
    query_id = 0
    avdl = doc_avdl()
    for query in queries:
        query_id += 1
        bm25_scores = bm25(query, query_id, avdl)
        write_scores_to_file(bm25_scores, query_id)


main()
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
    file = open('cacm.query.txt', 'r')
    queries = [""] * 65
    isText = False
    i = 0
    for line in file:
        if (len(line)) == 0:
            continue
        elif line[0] == '<' or (line[0] == ' ' and len(line) == 1):
            isText = False
            continue
        else:
            if not isText:
                isText = True
                queries[i] = ""
                queries[i] += line
                i += 1
            else:
                queries[i - 1] += " "
                queries[i - 1] += line
    for i in range(len(queries)):
        query = queries[i].lower()
        # handle punctuations
        queries[i] = regexp_tokenize(query, pattern='\w+')
    save_queries(queries)
    return queries[:-1]


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
#     files = glob(os.path.join('corpus', '*.txt'))
#     doc_list = []
#     rel_list = []
#     rels = open('cacm.rel.txt', 'r')
#     for rel in rels.readlines():
#         rel = rel.split()
#         if int(rel[0]) == query_id: doc_list.append(rel[2])
#         if int(rel[0]) > query_id: break
#     for file in files:
#         doc = file[:-5]
#         if doc in doc_list: rel_list.append(doc)
#     return rel_list
#
#
# def get_ri(doc_list, rel_list):
#     ri = 0
#     for doc in doc_list:
#         if doc in rel_list:
#             ri += 1
#     return ri


def write_scores_to_file(scores, query_id):
    file1 = open("results/query_expansion/bm25_query" + str(query_id) + ".txt", 'w')
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


# def get_frequent_terms(scores):
#     stopwords = get_stopwords()
#     freq_dict = {}
#     for item in scores:
#         doc_id = item[0]
#         text = open('./corpus/' + doc_id + '.txt').read()
#         for term in text.split():
#             if term in freq_dict:
#                 freq_dict[term] += 1
#             else:
#                 freq_dict[term] = 1
#     lst = sorted(freq_dict.items(), key=operator.itemgetter(1), reverse=True)
#     frequent_terms = [0] * 10
#     for i in range(10):
#         if lst[i][0] in stopwords:
#             i -= 1
#             continue
#         frequent_terms[i] = lst[i][0]
#     return frequent_terms


def get_stopwords():
    text = open('./common_words').read()
    return text.split()


def query_expansion(query, scores):
    stopwords = get_stopwords()
    init_weight = {}
    for term in query:
        if term in init_weight:
            init_weight[term] += 1
        else:
            init_weight[term] = 1
    terms = list(index.keys())
    rel_score = {}
    non_rel_score = {}
    rel_docs = set()
    term_score = {}
    for item in scores:
        doc_id = item[0]
        rel_docs.add(doc_id)
    for term in terms:
        non_rel_score[term] = sum(list(index[term].values()))
        if term not in init_weight:
            init_weight[term] = 0
    for term in terms:
        for doc_id in rel_docs:
            if doc_id not in index[term]:
                continue
            if term in rel_score:
                rel_score[term] += index[term][doc_id]
            else:
                rel_score[term] = index[term][doc_id]
            non_rel_score[term] -= index[term][doc_id]
    for term in terms:
        term_score[term] = 8 * init_weight[term] + 16 / 10 * rel_score.get(term, 0) - 4 / 3014 * non_rel_score[term]
    term_score = sorted(term_score.items(), key=lambda x: x[1], reverse=True)
    expand_query = []
    i = 0
    while len(expand_query) < 10:
        if term_score[i][0] in stopwords or term_score[i][0] in query:
            i += 1
            continue
        expand_query.append(term_score[i][0])
        i += 1
    return query + expand_query



def main():
    doc_length()
    generate_unigram()
    queries = get_queries()
    query_id = 0
    avdl = doc_avdl()
    top = 10
    for query in queries:
        query_id += 1
        # TOP 10 DOCS From Query Expansion
        bm25_scores = bm25(query, query_id, avdl)[0: top]
        # query expansion
        query = query_expansion(query, bm25_scores)
        bm25_scores = bm25(query, query_id, avdl)
        write_scores_to_file(bm25_scores, query_id)


main()
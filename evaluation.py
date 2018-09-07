##!/usr/bin/env python3
## -*- coding: utf-8 -*-
#"""
#Created on Fri Apr 20 14:37:20 2018
#
#@author: stian
#"""
#
# BM25 result


def write_to_txt(dict_name,title):
    f = open(title +'.txt','w')
    for key in dict_name:
        f.write(key+': '+'\n')
        f.write(str(dict_name[key]))
        f.write('\n')
        f.write('\n')
    f.close()



def get_full_name_rel():
    file = open('cacm.rel.fullname.txt', "w")
    rels = open('cacm.rel.txt', 'r')
    for rel in rels.readlines():
        rel = rel.split()
        if len(rel[2]) == 9:
            #print(rel)
            file.write(" ".join(rel) + "\n")
        elif len(rel[2]) == 8:
            tmp = rel[2]
            rel[2] = tmp[0:5] + "0" + tmp[5:]
            file.write(" ".join(rel) + "\n")
        else:
            tmp = rel[2]
            rel[2] = tmp[0:5] + "00" + tmp[5:]
            file.write(" ".join(rel) + "\n")
get_full_name_rel()

relevance = []
f = open("cacm.rel.fullname.txt",'r')
for i in f.readlines():
    relevance.append(i)
    
rel_dict = {}
for i in range(64):
    rel_dict[i+1] = []

queryID = 1
for i in range(len(relevance)):
    if relevance[i].split()[0] == str(queryID):
        rel_dict[queryID].append(relevance[i].split()[2][5:])
    else:
        queryID = int(relevance[i].split()[0])
        rel_dict[queryID].append(relevance[i].split()[2][5:])










bm25_table = {}   
for i in range(1, 65):
    tmp_docid_list = []
    f = open("results/bm25/bm25_query"+str(i)+".txt")
    for j in f.readlines():
        tmp_docid_list.append(int(j.split()[2][5:]))
    bm25_table[i] = tmp_docid_list
    f.close()
        
bm25_pr_table = {}
for i in range(1, 65):
    bm25_pr_table[i] = {}
    rel = 0
    total_rel = len(rel_dict[i])
    for j in range(1,101):
        bm25_pr_table[i][bm25_table[i][j-1]] = {}
        if total_rel == 0:
            bm25_pr_table[i][bm25_table[i][j-1]]['precision'] = rel/j
            bm25_pr_table[i][bm25_table[i][j-1]]['recall'] = 0
        elif str(bm25_table[i][j-1]) in rel_dict[i]:
            bm25_pr_table[i][bm25_table[i][j-1]]['precision'] = rel/j
            bm25_pr_table[i][bm25_table[i][j-1]]['recall'] = rel/total_rel
            rel+=1
        else:
            bm25_pr_table[i][bm25_table[i][j-1]]['precision'] = rel/j
            bm25_pr_table[i][bm25_table[i][j-1]]['recall'] = rel/total_rel


sum_map = 0
sum_ap = 0                                    
for i in range(1, 65):
    #sum_ap = 0
    if len(rel_dict[i]) == 0:
        continue        
    for docid in bm25_pr_table[i]:# in query i
        if str(docid) in rel_dict[i]:
            sum_ap += bm25_pr_table[i][docid]['precision'] 
    sum_map += sum_ap/100
MAP = sum_map/64


tot_rr = 0
for i in range(1, 65):
    rr = 0
    count = 0
    if len(rel_dict[i]) == 0:
        continue
    for docid in bm25_pr_table[i]:
        count+=1
        if str(docid) in rel_dict[i]:
            rr = 1/count
            break;
    tot_rr+=rr

MRR = tot_rr/64
      
p_at_k5 = {}
for query in bm25_pr_table:
    keys = []
    for key in bm25_pr_table[query]:
        keys.append(key)
    p_at_k5[query] = bm25_pr_table[query][keys[4]]['precision']
    

p_at_k20 = {}
for query in bm25_pr_table:
    keys = []
    for key in bm25_pr_table[query]:
        keys.append(key)
    p_at_k20[query] = bm25_pr_table[query][keys[19]]['precision']
    
    
bm25_dict = {}
bm25_dict['pr'] = bm25_pr_table
bm25_dict['MAP'] = MAP
bm25_dict['MRR'] = MRR
bm25_dict['P@K = 5'] = p_at_k5
bm25_dict['P@K =20'] = p_at_k20            
#
























          
#Query likelihood result

ql_table = {}   
for i in range(1, 65):
    tmp_docid_list = []
    f = open("results/query_likelihood/query_likelihood_query"+str(i)+".txt")
    for j in f.readlines():
        tmp_docid_list.append(int(j.split()[2][5:]))
    ql_table[i] = tmp_docid_list
    f.close()
        
ql_pr_table = {}
for i in range(1, 65):
    ql_pr_table[i] = {}
    rel = 0
    total_rel = len(rel_dict[i])
    for j in range(1,101):
        ql_pr_table[i][ql_table[i][j-1]] = {}
        if total_rel == 0:
            ql_pr_table[i][ql_table[i][j-1]]['precision'] = rel/j
            ql_pr_table[i][ql_table[i][j-1]]['recall'] = 0
        elif str(ql_table[i][j-1]) in rel_dict[i]:
            ql_pr_table[i][ql_table[i][j-1]]['precision'] = rel/j
            ql_pr_table[i][ql_table[i][j-1]]['recall'] = rel/total_rel
            rel+=1
        else:
            ql_pr_table[i][ql_table[i][j-1]]['precision'] = rel/j
            ql_pr_table[i][ql_table[i][j-1]]['recall'] = rel/total_rel

sum_map = 0  
sum_ap = 0                                  
for i in range(1, 65):
    
    if len(rel_dict[i]) == 0:
        continue        
    for docid in ql_pr_table[i]:# in query i
        if str(docid) in rel_dict[i]:
            sum_ap += ql_pr_table[i][docid]['precision'] 
    sum_map += sum_ap/100
MAP = sum_map/64

tot_rr = 0
for i in range(1, 65):
    rr = 0
    count = 0
    if len(rel_dict[i]) == 0:
        continue
    for docid in ql_pr_table[i]:
        count+=1
        if str(docid) in rel_dict[i]:
            rr = 1/count
            break;
    tot_rr+=rr

MRR = tot_rr/64
      
p_at_k5 = {}
for query in ql_pr_table:
    keys = []
    for key in ql_pr_table[query]:
        keys.append(key)
    p_at_k5[query] = ql_pr_table[query][keys[4]]['precision']
    

p_at_k20 = {}
for query in ql_pr_table:
    keys = []
    for key in ql_pr_table[query]:
        keys.append(key)
    p_at_k20[query] = ql_pr_table[query][keys[19]]['precision']   
    
ql_dict = {}
ql_dict['pr'] = ql_pr_table
ql_dict['MAP'] = MAP
ql_dict['MRR'] = MRR
ql_dict['P@K = 5'] = p_at_k5
ql_dict['P@K =20'] = p_at_k20     


















#Lucene result

lucene_table = {}   
for i in range(1, 65):
    tmp_docid_list = []
    f = open("results/lucene/task1query"+str(i)+".txt")
    for j in f.readlines():
        tmp_docid_list.append(int(j.split()[1][7:11]))
    lucene_table[i] = tmp_docid_list
    f.close()
        
lucene_pr_table = {}
for i in range(1, 65):
    lucene_pr_table[i] = {}
    rel = 0
    total_rel = len(rel_dict[i])
    for j in range(1,101):
        lucene_pr_table[i][lucene_table[i][j-1]] = {}
        if total_rel == 0:
            lucene_pr_table[i][lucene_table[i][j-1]]['precision'] = rel/j
            lucene_pr_table[i][lucene_table[i][j-1]]['recall'] = 0
        elif str(lucene_table[i][j-1]) in rel_dict[i]:
            lucene_pr_table[i][lucene_table[i][j-1]]['precision'] = rel/j
            lucene_pr_table[i][lucene_table[i][j-1]]['recall'] = rel/total_rel
            rel+=1
        else:
            lucene_pr_table[i][lucene_table[i][j-1]]['precision'] = rel/j
            lucene_pr_table[i][lucene_table[i][j-1]]['recall'] = rel/total_rel

sum_map = 0   
sum_ap = 0                                 
for i in range(1, 65):
    
    if len(rel_dict[i]) == 0:
        continue        
    for docid in lucene_pr_table[i]:# in query i
        if str(docid) in rel_dict[i]:
            sum_ap += lucene_pr_table[i][docid]['precision'] 
    sum_map += sum_ap/100
MAP = sum_map/64

tot_rr = 0
for i in range(1, 65):
    rr = 0
    count = 0
    if len(rel_dict[i]) == 0:
        continue
    for docid in lucene_pr_table[i]:
        count+=1
        if str(docid) in rel_dict[i]:
            rr = 1/count
            break;
    tot_rr+=rr

MRR = tot_rr/64
      
p_at_k5 = {}
for query in lucene_pr_table:
    keys = []
    for key in lucene_pr_table[query]:
        keys.append(key)
    p_at_k5[query] = lucene_pr_table[query][keys[4]]['precision']
    

p_at_k20 = {}
for query in lucene_pr_table:
    keys = []
    for key in lucene_pr_table[query]:
        keys.append(key)
    p_at_k20[query] = lucene_pr_table[query][keys[19]]['precision']   
    
lucene_dict = {}
lucene_dict['pr'] = lucene_pr_table
lucene_dict['MAP'] = MAP
lucene_dict['MRR'] = MRR
lucene_dict['P@K = 5'] = p_at_k5
lucene_dict['P@K =20'] = p_at_k20     
















#query expansion result

expansion_table = {}   
for i in range(1, 65):
    tmp_docid_list = []
    f = open("results/query_expansion/bm25_query"+str(i)+".txt")
    for j in f.readlines():
        tmp_docid_list.append(int(j.split()[2][5:]))
    expansion_table[i] = tmp_docid_list
    f.close()
        
expansion_pr_table = {}
for i in range(1, 65):
    expansion_pr_table[i] = {}
    rel = 0
    total_rel = len(rel_dict[i])
    for j in range(1,101):
        expansion_pr_table[i][expansion_table[i][j-1]] = {}
        if total_rel == 0:
            expansion_pr_table[i][expansion_table[i][j-1]]['precision'] = rel/j
            expansion_pr_table[i][expansion_table[i][j-1]]['recall'] = 0
        elif str(expansion_table[i][j-1]) in rel_dict[i]:
            expansion_pr_table[i][expansion_table[i][j-1]]['precision'] = rel/j
            expansion_pr_table[i][expansion_table[i][j-1]]['recall'] = rel/total_rel
            rel+=1
        else:
            expansion_pr_table[i][expansion_table[i][j-1]]['precision'] = rel/j
            expansion_pr_table[i][expansion_table[i][j-1]]['recall'] = rel/total_rel

sum_map = 0   
sum_ap = 0                                 
for i in range(1, 65):
    
    if len(rel_dict[i]) == 0:
        continue        
    for docid in expansion_pr_table[i]:# in query i
        if str(docid) in rel_dict[i]:
            sum_ap += expansion_pr_table[i][docid]['precision'] 
    sum_map += sum_ap/100
MAP = sum_map/64

tot_rr = 0
for i in range(1, 65):
    rr = 0
    count = 0
    if len(rel_dict[i]) == 0:
        continue
    for docid in expansion_pr_table[i]:
        count+=1
        if str(docid) in rel_dict[i]:
            rr = 1/count
            break;
    tot_rr+=rr

MRR = tot_rr/64
      
p_at_k5 = {}
for query in expansion_pr_table:
    keys = []
    for key in expansion_pr_table[query]:
        keys.append(key)
    p_at_k5[query] = expansion_pr_table[query][keys[4]]['precision']
    

p_at_k20 = {}
for query in expansion_pr_table:
    keys = []
    for key in expansion_pr_table[query]:
        keys.append(key)
    p_at_k20[query] = expansion_pr_table[query][keys[19]]['precision']   
    
expansion_dict = {}
expansion_dict['pr'] = expansion_pr_table
expansion_dict['MAP'] = MAP
expansion_dict['MRR'] = MRR
expansion_dict['P@K = 5'] = p_at_k5
expansion_dict['P@K =20'] = p_at_k20     


















# bm25 stop result
bm25_stop_table = {}   
for i in range(1, 65):
    tmp_docid_list = []
    f = open("results/bm25_stopped/bm25_query"+str(i)+".txt")
    for j in f.readlines():
        tmp_docid_list.append(int(j.split()[2][5:]))
    bm25_stop_table[i] = tmp_docid_list
    f.close()
        
bm25_stop_pr_table = {}
for i in range(1, 65):
    bm25_stop_pr_table[i] = {}
    rel = 0
    total_rel = len(rel_dict[i])
    for j in range(1,101):
        bm25_stop_pr_table[i][bm25_stop_table[i][j-1]] = {}
        if total_rel == 0:
            bm25_stop_pr_table[i][bm25_stop_table[i][j-1]]['precision'] = rel/j
            bm25_stop_pr_table[i][bm25_stop_table[i][j-1]]['recall'] = 0
        elif str(bm25_stop_table[i][j-1]) in rel_dict[i]:
            bm25_stop_pr_table[i][bm25_stop_table[i][j-1]]['precision'] = rel/j
            bm25_stop_pr_table[i][bm25_stop_table[i][j-1]]['recall'] = rel/total_rel
            rel+=1
        else:
            bm25_stop_pr_table[i][bm25_stop_table[i][j-1]]['precision'] = rel/j
            bm25_stop_pr_table[i][bm25_stop_table[i][j-1]]['recall'] = rel/total_rel

sum_map = 0 
sum_ap = 0                                   
for i in range(1, 65):
    
    if len(rel_dict[i]) == 0:
        continue        
    for docid in bm25_stop_pr_table[i]:# in query i
        if str(docid) in rel_dict[i]:
            sum_ap += bm25_stop_pr_table[i][docid]['precision'] 
    sum_map += sum_ap/100
MAP = sum_map/64

tot_rr = 0
for i in range(1, 65):
    rr = 0
    count = 0
    if len(rel_dict[i]) == 0:
        continue
    for docid in bm25_stop_pr_table[i]:
        count+=1
        if str(docid) in rel_dict[i]:
            rr = 1/count
            break;
    tot_rr+=rr

MRR = tot_rr/64
      
p_at_k5 = {}
for query in bm25_stop_pr_table:
    keys = []
    for key in bm25_stop_pr_table[query]:
        keys.append(key)
    p_at_k5[query] = bm25_stop_pr_table[query][keys[4]]['precision']
    

p_at_k20 = {}
for query in bm25_stop_pr_table:
    keys = []
    for key in bm25_stop_pr_table[query]:
        keys.append(key)
    p_at_k20[query] = bm25_stop_pr_table[query][keys[19]]['precision']   
    
bm25_stop_dict = {}
bm25_stop_dict['pr'] = bm25_stop_pr_table
bm25_stop_dict['MAP'] = MAP
bm25_stop_dict['MRR'] = MRR
bm25_stop_dict['P@K = 5'] = p_at_k5
bm25_stop_dict['P@K =20'] = p_at_k20     



















# ql stop result
ql_stop_table = {}   
for i in range(1, 65):
    tmp_docid_list = []
    f = open("results/query_likelihood_stopped/query_likelihood_query"+str(i)+".txt")
    for j in f.readlines():
        tmp_docid_list.append(int(j.split()[2][5:]))
    ql_stop_table[i] = tmp_docid_list
    f.close()
        
ql_stop_pr_table = {}
for i in range(1, 65):
    ql_stop_pr_table[i] = {}
    rel = 0
    total_rel = len(rel_dict[i])
    for j in range(1,101):
        ql_stop_pr_table[i][ql_stop_table[i][j-1]] = {}
        if total_rel == 0:
            ql_stop_pr_table[i][ql_stop_table[i][j-1]]['precision'] = rel/j
            ql_stop_pr_table[i][ql_stop_table[i][j-1]]['recall'] = 0
        elif str(ql_stop_table[i][j-1]) in rel_dict[i]:
            ql_stop_pr_table[i][ql_stop_table[i][j-1]]['precision'] = rel/j
            ql_stop_pr_table[i][ql_stop_table[i][j-1]]['recall'] = rel/total_rel
            rel+=1
        else:
            ql_stop_pr_table[i][ql_stop_table[i][j-1]]['precision'] = rel/j
            ql_stop_pr_table[i][ql_stop_table[i][j-1]]['recall'] = rel/total_rel

sum_map = 0
sum_ap = 0                                    
for i in range(1, 65):
    
    if len(rel_dict[i]) == 0:
        continue        
    for docid in ql_stop_pr_table[i]:# in query i
        if str(docid) in rel_dict[i]:
            sum_ap += ql_stop_pr_table[i][docid]['precision'] 
    sum_map += sum_ap/100
MAP = sum_map/64

tot_rr = 0
for i in range(1, 65):
    rr = 0
    count = 0
    if len(rel_dict[i]) == 0:
        continue
    for docid in ql_stop_pr_table[i]:
        count+=1
        if str(docid) in rel_dict[i]:
            rr = 1/count
            break;
    tot_rr+=rr

MRR = tot_rr/64
      
p_at_k5 = {}
for query in ql_stop_pr_table:
    keys = []
    for key in ql_stop_pr_table[query]:
        keys.append(key)
    p_at_k5[query] = ql_stop_pr_table[query][keys[4]]['precision']
    

p_at_k20 = {}
for query in ql_stop_pr_table:
    keys = []
    for key in ql_stop_pr_table[query]:
        keys.append(key)
    p_at_k20[query] = ql_stop_pr_table[query][keys[19]]['precision']   
    
ql_stop_dict = {}
ql_stop_dict['pr'] = ql_stop_pr_table
ql_stop_dict['MAP'] = MAP
ql_stop_dict['MRR'] = MRR
ql_stop_dict['P@K = 5'] = p_at_k5
ql_stop_dict['P@K =20'] = p_at_k20     














# tf-idf stop result
tfidf_stop_table = {}   
for i in range(1, 65):
    tmp_docid_list = []
    f = open("results/tf_idf_stopped/tf_idf_query"+str(i)+".txt")
    for j in f.readlines():
        tmp_docid_list.append(int(j.split()[2][5:]))
    tfidf_stop_table[i] = tmp_docid_list
    f.close()
        
tfidf_stop_pr_table = {}
for i in range(1, 65):
    tfidf_stop_pr_table[i] = {}
    rel = 0
    total_rel = len(rel_dict[i])
    for j in range(1,101):
        tfidf_stop_pr_table[i][tfidf_stop_table[i][j-1]] = {}
        if total_rel == 0:
            tfidf_stop_pr_table[i][tfidf_stop_table[i][j-1]]['precision'] = rel/j
            tfidf_stop_pr_table[i][tfidf_stop_table[i][j-1]]['recall'] = 0
        elif str(tfidf_stop_table[i][j-1]) in rel_dict[i]:
            tfidf_stop_pr_table[i][tfidf_stop_table[i][j-1]]['precision'] = rel/j
            tfidf_stop_pr_table[i][tfidf_stop_table[i][j-1]]['recall'] = rel/total_rel
            rel+=1
        else:
            tfidf_stop_pr_table[i][tfidf_stop_table[i][j-1]]['precision'] = rel/j
            tfidf_stop_pr_table[i][tfidf_stop_table[i][j-1]]['recall'] = rel/total_rel

sum_map = 0 
sum_ap = 0                                   
for i in range(1, 65):
    
    if len(rel_dict[i]) == 0:
        continue        
    for docid in tfidf_stop_pr_table[i]:# in query i
        if str(docid) in rel_dict[i]:
            sum_ap += tfidf_stop_pr_table[i][docid]['precision'] 
    sum_map += sum_ap/100
MAP = sum_map/64

tot_rr = 0
for i in range(1, 65):
    rr = 0
    count = 0
    if len(rel_dict[i]) == 0:
        continue
    for docid in tfidf_stop_pr_table[i]:
        count+=1
        if str(docid) in rel_dict[i]:
            rr = 1/count
            break;
    tot_rr+=rr

MRR = tot_rr/64
      
p_at_k5 = {}
for query in tfidf_stop_pr_table:
    keys = []
    for key in tfidf_stop_pr_table[query]:
        keys.append(key)
    p_at_k5[query] = tfidf_stop_pr_table[query][keys[4]]['precision']
    

p_at_k20 = {}
for query in tfidf_stop_pr_table:
    keys = []
    for key in tfidf_stop_pr_table[query]:
        keys.append(key)
    p_at_k20[query] = tfidf_stop_pr_table[query][keys[19]]['precision']   
    
tfidf_stop_dict = {}
tfidf_stop_dict['pr'] = tfidf_stop_pr_table
tfidf_stop_dict['MAP'] = MAP
tfidf_stop_dict['MRR'] = MRR
tfidf_stop_dict['P@K = 5'] = p_at_k5
tfidf_stop_dict['P@K =20'] = p_at_k20     












#TF-IDF result

tfidf_table = {}   
for i in range(1, 65):
    tmp_docid_list = []
    f = open("results/tf_idf/tf_idf_query"+str(i)+".txt")
    for j in f.readlines():
        tmp_docid_list.append(int(j.split()[2][5:]))
    tfidf_table[i] = tmp_docid_list
    f.close()
        
tfidf_pr_table = {}
for i in range(1, 65):
    tfidf_pr_table[i] = {}
    rel = 0
    total_rel = len(rel_dict[i])
    for j in range(1,101):
        tfidf_pr_table[i][tfidf_table[i][j-1]] = {}
        if total_rel == 0:
            tfidf_pr_table[i][tfidf_table[i][j-1]]['precision'] = rel/j
            tfidf_pr_table[i][tfidf_table[i][j-1]]['recall'] = 0
        elif str(tfidf_table[i][j-1]) in rel_dict[i]:
            tfidf_pr_table[i][tfidf_table[i][j-1]]['precision'] = rel/j
            tfidf_pr_table[i][tfidf_table[i][j-1]]['recall'] = rel/total_rel
            rel+=1
        else:
            tfidf_pr_table[i][tfidf_table[i][j-1]]['precision'] = rel/j
            tfidf_pr_table[i][tfidf_table[i][j-1]]['recall'] = rel/total_rel

sum_map = 0
sum_ap = 0                                    
for i in range(1, 65):
    
    if len(rel_dict[i]) == 0:
        continue        
    for docid in tfidf_pr_table[i]:# in query i
        if str(docid) in rel_dict[i]:
            sum_ap += tfidf_pr_table[i][docid]['precision'] 
    sum_map += sum_ap/100
MAP = sum_map/64

tot_rr = 0
for i in range(1, 65):
    rr = 0
    count = 0
    if len(rel_dict[i]) == 0:
        continue
    for docid in tfidf_pr_table[i]:
        count+=1
        if str(docid) in rel_dict[i]:
            rr = 1/count
            break;
    tot_rr+=rr

MRR = tot_rr/64
      
p_at_k5 = {}
for query in tfidf_pr_table:
    keys = []
    for key in tfidf_pr_table[query]:
        keys.append(key)
    p_at_k5[query] = tfidf_pr_table[query][keys[4]]['precision']
    

p_at_k20 = {}
for query in tfidf_pr_table:
    keys = []
    for key in tfidf_pr_table[query]:
        keys.append(key)
    p_at_k20[query] = tfidf_pr_table[query][keys[19]]['precision']   
    
tfidf_dict = {}
tfidf_dict['pr'] = tfidf_pr_table
tfidf_dict['MAP'] = MAP
tfidf_dict['MRR'] = MRR
tfidf_dict['P@K = 5'] = p_at_k5
tfidf_dict['P@K =20'] = p_at_k20     












write_to_txt(bm25_dict,'bm25_evaluation')
write_to_txt(ql_dict,'query_likelihood_evaluation')
write_to_txt(lucene_dict,'lucene_evaluation')
write_to_txt(expansion_dict,'expansion_evaluation')
write_to_txt(bm25_stop_dict,'bm25_stop_evaluation')
write_to_txt(ql_stop_dict,'ql_stop_evaluation')
write_to_txt(tfidf_dict,'tf_idf_evaluation')
write_to_txt(tfidf_stop_dict,'tf_idf_stop_evaluation')






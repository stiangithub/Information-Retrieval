#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:04:59 2018

@author: stian
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 19:23:21 2018

@author: Di Yi
"""
f= open("cacm_stem.txt",'r')

stem_corpus = []
for i in f.readlines():
    stem_corpus.append(i)
for i in range(len(stem_corpus)):
    stem_corpus[i] = stem_corpus[i].split()
f.close()    
boundry = []
for i in range(len(stem_corpus)):
    if "#" in stem_corpus[i]:
        boundry.append(i)
stem_corpus_dict = {}
for i in range(len(boundry)-1):
    stem_corpus_dict[i] = stem_corpus[boundry[i]+1:boundry[i+1]]
stem_corpus_dict[3203] = stem_corpus[boundry[3203]+1:]   



for i in range(len(stem_corpus_dict)):
    s = ''
    for value in stem_corpus_dict[i]:
        for term in value:
            s+=term+' '
        
    stem_corpus_dict[i] = s
    for ite in range(len(s.split())):
        if s.split()[ite] in ['pm','am']:
            stem_corpus_dict[i] = s.split()[0:ite+1]

         

for i in range(len(stem_corpus_dict)):
    new_item = ''
    for j in stem_corpus_dict[i]:
        new_item += j+' '
    stem_corpus_dict[i] = new_item
    if i in range(0,9):
        f = open("stem_corpus/"+'000'+str(i+1)+'.txt','w')
    if i in range(9,99):
        f = open("stem_corpus/"+'00'+str(i+1)+'.txt','w')
    if i in range(99,999):
        f = open("stem_corpus/"+'0'+str(i+1)+'.txt','w')
    if i in range(999,len(stem_corpus_dict)):
        f = open("stem_corpus/"+str(i+1)+'.txt','w') 
    
    
    f.write(stem_corpus_dict[i])
    f.close()
            
       
        


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:20:21 2018

@author: stian
"""

f = open("results/bm25/bm25_query10.txt",'r')
score = []
for i in f.readlines():
    score.append(float(i.split()[4]))
average_score = sum(score)/len(score)
f.close()
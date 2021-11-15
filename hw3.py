import os,sys
import nltk
import re
import math
import numpy as np
import csv

nltk.download('stopwords')
import matplotlib.pyplot as plt
import difflib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models import word2vec
#import random

#folder_path = QFileDialog.getExistingDirectory(self,"Open folder","./")
#folder_path="./hw2_data"
folder_path="./constact"
#folder_path="./test"
files= os.listdir(folder_path) #得到資料夾下的所有檔名稱

top = int(input("請輸入欲顯示詞頻Top數:"))
key = str(input("請輸入欲查詢關鍵字:"))
count= int(input("請輸入欲讀取文章數:"))
counts=0
#去除停用字統計文章字頻
stopword = stopwords.words('english')
STR_nostopwords=[]
SimilarKey={}
TOL_STR=[]
# Settings
#seed = 6 #亂數種子
sg = 1 #演算法，預設為0，代表是CBOW，若設為1則是使用Skip-Gram
window_size = 10 #周圍詞彙要看多少範圍
vector_size = round(count/3) #轉成向量的維度，維度太小會無法有效表達詞與詞的關係，維度太大會使關係太稀疏而難以找出規則
min_count = round(count/10) #該詞最少出現幾次，才可以被當作是訓練資料
workers = 8 #訓練的並行數量
epochs = 8 #訓練的迭代次數
batch_words = round(count/3) #每次給予多少詞彙量訓練



#統計每篇文章字頻
for file in files: #遍歷資料夾
    if not os.path.isdir(file): #判斷是否是資料夾,不是資料夾才打開
        if counts==count:
            break
        else:
                file_path=folder_path+"/"+file
                nm = os.path.splitext(file_path)
                try:
                    file = open(file_path, 'r',encoding="utf-8")
                except FileNotFoundError:
                    print(file_path + '不存在')
                    sys.exit(1)
                except PermissionError:
                    print(file_path + '不是檔案')
                    sys.exit(1)
                else:
                    if nm[1]==".txt":
                        abstract=file.read()
                        mark_out = re.sub(r'[^\w\s]','',abstract.replace('/', ' '))
                        Awords=word_tokenize(mark_out.lower())#變小寫
                        for w in Awords:     
                            if w in stopword: continue
                            else:
                                seq = difflib.SequenceMatcher(None,key,w)
                                ratio=seq.ratio()
                                if ratio>=0.75:
                                    if w in SimilarKey: continue
                                    else:
                                        SimilarKey[w]=ratio
                                    w=key
                                #print('ratio:'+str(ratio)) 
                                STR_nostopwords.append(w)
                        TOL_STR.append(STR_nostopwords)    
                        file.close()
                    else:
                         print(file_path+"檔案類型不符，此檔案不解析\n")
                         continue
    counts=counts+1
model = word2vec.Word2Vec(
                                    TOL_STR,
                                    min_count=min_count,
                                    vector_size=vector_size,
                                    workers=workers,
                                    epochs=epochs,
                                    window=window_size,
                                    sg=sg,
                                    #seed=seed,
                                    batch_words=batch_words
                             )  
print('stopword:'+str(len(stopword)))
print('SimilarKey:')
print(SimilarKey)
model.save('word2vec.model')
models = word2vec.Word2Vec.load('word2vec.model')
#print(models.wv['endometriosis'].shape)
#print(models.wv.most_similar(key))
print('SG')
for item in models.wv.similar_by_word(key, topn =top-1):
    print(item)


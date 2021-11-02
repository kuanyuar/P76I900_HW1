import os,sys
import nltk
import re
import math
import numpy as np
import csv
#import xml.etree.ElementTree as ET
#nltk.download('punkt')
nltk.download('stopwords')
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
#from scipy import special  # doctest:+SKIP
#from sklearn.feature_extraction.text import TfidfVectorizer
#import random

#folder_path = QFileDialog.getExistingDirectory(self,"Open folder","./")
#folder_path="./hw2_data"
folder_path="./test"
#key=str(self.textEdit.toPlainText())
files= os.listdir(folder_path) #得到資料夾下的所有檔名稱
#article=[]
#index=0
#str1=""
db = np.empty( (10,), dtype=[('title',object),('wordcounts',object)] )
cnt=0
counts=0
#總統計文章字頻
words=[]
wordcounts={}
#去除停用字統計文章字頻
stopword = stopwords.words('english')
nostopwords=[]
nostopword_count={}
porter_stemmer = PorterStemmer()
porter_words=[]
porter_counts={}
df={}

#統計每篇文章字頻
for file in files: #遍歷資料夾
    if not os.path.isdir(file): #判斷是否是資料夾,不是資料夾才打開
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
                    if nm[1]==".csv":
                        Reader = csv.DictReader(file)
                        mycsv = list(Reader)
                        for n in range(len(mycsv)) :
                            #row = rows
                            if(str(mycsv[n]['abstract'])==''):
                                abstract=str(mycsv[n]['title'])
                                #print(file_path+":"+str(mycsv[n]['title']))
                            else:
                                abstract=str(mycsv[n]['abstract'])
                            mark_out = re.sub(r'[^\w\s]','',abstract.replace('/', ' '))
                            words=word_tokenize(mark_out.lower())#變小寫
                            wordcount={}
                            word=[]
                            for w in words:
                                counts+=1
                                if not w in word :
                                    word.append(w)
                                if not w in wordcount:
                                    wordcount[w] = 1
                                else:
                                    wordcount[w] += 1
                                    
                                if not w in words :
                                    words.append(w)
                                if not w in wordcounts:
                                    wordcounts[w] = 1
                                else:
                                    wordcounts[w] += 1
                                    
                                if w in stopword: continue
                                elif not w in nostopwords :
                                    nostopwords.append(w)
                                    nostopword_count[w] = 1
                                else:
                                    nostopword_count[w] += 1
                                
                                if w in stopword: continue
                                elif not porter_stemmer.stem(w) in porter_words :
                                    porter_words.append(porter_stemmer.stem(w))
                                    porter_counts[porter_stemmer.stem(w)] = 1
                                 #if n==0:
                                 # df[porter_stemmer.stem(w)]=1
                                 #elif df[porter_stemmer.stem(w)]=='':
                                 #df[porter_stemmer.stem(w)]=1
                                 #else:
                                 #df[porter_stemmer.stem(w)] += 1
                                else:
                                    #print ("Actual: %s  Stem: %s"  % (str(label[i]),porter_stemmer.stem(str(label[i]))))
                                    porter_counts[porter_stemmer.stem(w)] += 1
                            counter_list = sorted(wordcount.items(), key=lambda x: x[1], reverse=True)
                            #print(str(n)+':'+str(mycsv[n]['title']))
                            db['title'][cnt]=str(mycsv[n]['title'])
                            db['wordcounts'][cnt]=counter_list
                            cnt=cnt+1
                            
                        file.close()
                    else:
                         print(file_path+"檔案類型不符，此檔案不解析\n")
                         continue


tol_counter_list = sorted(wordcounts.items(), key=lambda x: x[1], reverse=True)    
#for i in 
print('words:'+str(len(words)))#單詞數
print(tol_counter_list[:20])
        #for i,j in counter_list[:50]:print i

label = list(map(lambda x: x[0], tol_counter_list[:]))
value = list(map(lambda y: y[1], tol_counter_list[:]))
#counts=sum(value)
print('counts:'+str(counts))#總字數

plt.subplot(2, 2, 1)                 # plt.subplot(列數, 行數, 圖形編號)設定第一張圖位置
#plt.bar(range(len(org_value)), org_value, tick_label=org_label)
plt.plot(label,value)
plt.xticks(rotation=270)
plt.title('Unprocessed chart')
plt.ylabel('Frequency of words')
plt.xlabel('Words by rank order')
plt.show()

nostopword_counter_list = sorted(nostopword_count.items(), key=lambda x: x[1], reverse=True) 
#print(stopword)

print(nostopword_counter_list[:20])

label = list(map(lambda x: x[0], nostopword_counter_list[:]))
value = list(map(lambda y: y[1], nostopword_counter_list[:]))
print("nostopword:"+str(len(label)))
plt.subplot(2, 2, 2)                
plt.plot(label,value)
plt.xticks(rotation=270)
plt.title('Without stopwords chart')
plt.ylabel('Frequency of words')
plt.xlabel('Words by rank order')
plt.show()


        
porter_counter_list = sorted(porter_counts.items(), key=lambda x: x[1], reverse=True)    

print('porter_words:'+str(len(porter_words)))#單詞數
print(porter_counter_list[:20])


label = list(map(lambda x: x[0], porter_counter_list[:]))
value = list(map(lambda y: y[1], porter_counter_list[:]))

plt.subplot(2, 2, 3)                 
#plt.bar(range(len(value)), value, tick_label=label)
plt.plot(label,value)
plt.xticks(rotation=270)
plt.title('porter chart Without stopwords')
plt.ylabel('Frequency of words')
plt.xlabel('Words by rank order')
plt.show()

# tf-idf
tf=[]
idf=[]
tf_idf={}
for i in range(len(porter_words)):
    word_tf=int(porter_counts[porter_words[i]])/counts
    tf.append(int(word_tf))
    #print(porter_words[i]+":"+str(sum([1 for x in range(len(db))for y in range(len(db['wordcounts'][x])) if porter_words[i] in porter_stemmer.stem(str(db['wordcounts'][x][y][0]))])+1))
    word_idf=math.log10(10000/sum([1 for x in range(len(db))for y in range(len(db['wordcounts'][x])) if porter_words[i] in porter_stemmer.stem(str(db['wordcounts'][x][y][0]))])+1)
    #word_idf=math.log10(10000/df[porter_words[i]]+1)
    idf.append(int(word_idf))
    tf_idf[porter_words[i]]=word_tf*word_idf
tf_idf_counter_list = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)  
print(tf_idf_counter_list[0:20])
'''label = list(map(lambda x: x[0], label[:20]))
value = list(map(lambda y: y[1], tf_idf[:20]))
plt.subplot(2, 2, 4) 
plt.plot(label,value)
plt.xticks(rotation=270)
plt.title('tf-idf chart ')
plt.show()'''
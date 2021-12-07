import os,sys
import nltk
import re
import math
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
#import adjustText

nltk.download('stopwords')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from gensim.models import word2vec
#from sklearn.decomposition import PCA
#from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib
from mpl_toolkits import mplot3d
#folder_path = QFileDialog.getExistingDirectory(self,"Open folder","./")
folder_path="./hw3-2data"
#folder_path="./test"
#文件夾下所以檔案數
files= os.listdir(folder_path) #得到資料夾下的所有檔名稱
all_content=os.listdir(folder_path)
#print('All content numbers is',len(all_content))
cnts=len(all_content)
top = int(input("請輸入欲顯示詞頻Top數:"))
key = str(input("請輸入欲查詢關鍵字:"))

#去除停用字統計文章字頻
stopword = stopwords.words('english')
STR_nostopwords=[]
TOL_STR=[]
cnt=0
counts=0
#總統計文章字頻
words=[]
wordcounts={}
#去除停用字統計文章字頻
stopword = stopwords.words('english')
nostopwords=[]
nostopword_count={}
df_word=[]
df={}
sf_word=[]
sf={}
key_path=[]
sentences = np.empty( (cnts,), dtype=[('fileName',object),('sentence',object)] )#每篇文章記錄
S_TF_IDF={}
S_TF_ISF={}
STR_nostopwords=[]
TOL_STR=[]
# Settings
seed = 1 #亂數種子
sg = 1 #演算法，預設為0，代表是CBOW，若設為1則是使用Skip-Gram
window_size = 5 #周圍詞彙要看多少範圍
vector_size = 50 #轉成向量的維度，維度太小會無法有效表達詞與詞的關係，維度太大會使關係太稀疏而難以找出規則
min_count = 3 #該詞最少出現幾次，才可以被當作是訓練資料
workers = 4 #訓練的並行數量
epochs = 10 #訓練的迭代次數
batch_words = 100 #每次給予多少詞彙量訓練


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
                    if nm[1]==".txt":
                        abstract=file.read()
                        mark_out = re.sub(r'[^\w\s]','',abstract.replace('/', ' '))
                        sentence = sent_tokenize(abstract)
                        Awords=word_tokenize(mark_out.lower())#變小寫
                        '''for w in Awords:     
                            if w in stopword: continue
                            else:
                                STR_nostopwords.append(w)
                        TOL_STR.append(STR_nostopwords)'''
                        #詞頻
                        wordcount={}
                        word=[]
                        for w in Awords:
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
                                    STR_nostopwords.append(w)
                                else:
                                    nostopword_count[w] += 1
                                    STR_nostopwords.append(w)
                        for w in word:
                                if w in stopword: continue
                                elif not w in df_word :
                                    df_word.append(w)
                                    df[w] = 1
                                else:
                                    #print ("Actual: %s  Stem: %s"  % (str(label[i]),porter_stemmer.stem(str(label[i]))))
                                    df[w] += 1
                        TOL_STR.append(STR_nostopwords)        
                        counter_list = sorted(wordcount.items(), key=lambda x: x[1], reverse=True)
                        sentences['fileName'][cnt]=nm[0]
                        #print(sentences['fileName'][cnt])
                        #print('sentence:'+str(len(sentence)))
                        sentences['sentence'][cnt]=sentence
                        cnt=cnt+1
                        file.close()
                    else:
                         print(file_path+"檔案類型不符，此檔案不解析\n")
                         continue

tol_counter_list = sorted(wordcounts.items(), key=lambda x: x[1], reverse=True)    
#for i in 
if cnt==cnts:
    print("文章篇數:"+str(cnt))
else:
    print("檔案中有"+str(cnts-cnt)+"份文件無法正常讀取")
print('counts:'+str(counts))#總字數
print('words:'+str(len(words)))#單詞數
print("總辭頻Top"+str(top)+":")
print(tol_counter_list[:top])
#print("總辭頻Top"+str(top)+":"+tol_counter_list[:top])
        #for i,j in counter_list[:50]:print i

#counts=sum(value)



nostopword_counter_list = sorted(nostopword_count.items(), key=lambda x: x[1], reverse=True) 
print("nostopword Top"+str(top)+":")
print(nostopword_counter_list[:top])
label = list(map(lambda x: x[0], nostopword_counter_list[:top]))
value = list(map(lambda y: y[1], nostopword_counter_list[:top]))
print("nostopword:"+str(len(nostopwords)))              
plt.plot(label,value)
plt.xticks(rotation=270)
plt.title('Without stopwords chart')
plt.ylabel('Frequency of words')
plt.xlabel('Words by rank order')
plt.show()




# tf-idf
tf=[]
idf=[]
tf_idf={}
df_counter_list = sorted(df.items(), key=lambda x: x[1], reverse=True)  
print("df Top"+str(top)+":")
print(df_counter_list[:top])
for i in range(len(nostopwords)):
    word_tf=int(nostopword_count[nostopwords[i]])/counts
    tf.append(int(word_tf))
    #print(porter_words[i]+":"+str(sum([1 for x in range(len(db))for y in range(len(db['wordcounts'][x])) if porter_words[i] in porter_stemmer.stem(str(db['wordcounts'][x][y][0]))])+1))
    #word_idf=math.log10(10000/sum([1 for x in range(len(db))for y in range(len(db['wordcounts'][x])) if porter_words[i] in porter_stemmer.stem(str(db['wordcounts'][x][y][0]))])+1)
    word_idf=math.log10(cnt/df[nostopwords[i]]+1)
    idf.append(int(word_idf))
    tf_idf[nostopwords[i]]=word_tf*word_idf
tf_idf_counter_list = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)  
print("tf_idfTop"+str(top)+":")
print(tf_idf_counter_list[0:top])
#print("關鍵字出現於以下文章中")
#print(key_path)
print("關鍵字詞頻權重"+str(tf_idf[key]))
test=[]
#print('len(sentences)'+str(len(sentences)))
sentence=0#總句數
for i in range(len(sentences)):
    #print(sentences['fileName'][i])
    sentence+=len(sentences['sentence'][i])
    for j in range(len(sentences['sentence'][i])):
        #print(str(sentences['sentence'][i][j]))
        mark_out = re.sub(r'[^\w\s]','',sentences['sentence'][i][j].replace('/', ' '))
        Swords=word_tokenize(mark_out.lower())#變小寫
        s_tf_idf=0
        word=[]
        for w in Swords:
            if w in nostopwords:
                '''if w=='reduce':
                    print(str(sentences['sentence'][i][j]))'''
                #print(w+":")
                s_tf_idf+=tf_idf[w]
                #print(tf_idf[w])
                if not w in word :
                    word.append(w)
        for w in word:
            if not w in sf_word :
                sf_word.append(w)
                sf[w] = 1
            else:
                sf[w] += 1
        test.append([str(sentences['fileName'][i]),str(sentences['sentence'][i][j]),float(s_tf_idf/len(Swords))])
        S_TF_IDF[sentences['sentence'][i][j]]=s_tf_idf/len(Swords)#避免字數過多之句子影響權重，取平均
sf_counter_list = sorted(sf.items(), key=lambda x: x[1], reverse=True)  
print("總句子數:"+str(sentence))
print("sf Top"+str(top)+":")
#print(len(sf_counter_list))
print(sf_counter_list[:top])
#print(sf_counter_list)
isf=[]
tf_isf={}

for i in range(len(nostopwords)):
    word_tf=int(nostopword_count[nostopwords[i]])/counts
    #tf.append(int(word_tf))
    #print(str(nostopwords[i]))
    #print(str(sf[nostopwords[i]]))
    word_isf=math.log10(sentence/sf[nostopwords[i]]+1)
    isf.append(int(word_isf))
    tf_isf[nostopwords[i]]=word_tf*word_isf
tf_isf_counter_list = sorted(tf_isf.items(), key=lambda x: x[1], reverse=True)  
print("tf_isfTop"+str(top)+":")
print(tf_isf_counter_list[0:top])
test.sort(key=lambda x: x[2], reverse=True)
#print(test[0:2])
S_TF_IDF_list = sorted(S_TF_IDF.items(), key=lambda x: x[1], reverse=True) 
print("句子TF-IDF Top"+str(top)+":")
'''for i in range(0,top):
    #print(sentences.where(sentences['sentence']==S_TF_IDF_list[i][0]))
    #print(S_TF_IDF_list[i][0])
    print(S_TF_IDF_list[i])'''
for i in range(0,top):
    #print(test[i])
    print(test[i][1])
SEC=[]
for i in range(len(sentences)):
    #print(sentences['fileName'][i])
    for j in range(len(sentences['sentence'][i])):        
        #print(str(sentences['sentence'][i][j]))
        mark_out = re.sub(r'[^\w\s]','',sentences['sentence'][i][j].replace('/', ' '))
        Swords=word_tokenize(mark_out.lower())#變小寫
        s_tf_isf=0
        for w in Swords:
            if w in nostopwords:
                #print(w+":")
                s_tf_isf+=tf_isf[w]
                #print(tf_isf[w])
        SEC.append([str(sentences['fileName'][i]),str(sentences['sentence'][i][j]),float(s_tf_isf/len(Swords))])
        S_TF_ISF[sentences['sentence'][i][j]]=s_tf_isf/len(Swords)#避免字數過多之句子影響權重，取平均
SEC.sort(key=lambda x: x[2], reverse=True)
print("句子TF_ISF Top"+str(top)+":")
'''for i in range(0,top):
    #print(sentences.where(sentences['sentence']==S_TF_IDF_list[i][0]))
    #print(S_TF_IDF_list[i][0])
    print(S_TF_IDF_list[i])'''
for i in range(0,top):
    #print(SEC[i])
    print(SEC[i][1])
model = word2vec.Word2Vec(
                                    TOL_STR,
                                    min_count=min_count,
                                    vector_size=vector_size,
                                    workers=workers,
                                    epochs=epochs,
                                    window=window_size,
                                    sg=sg,
                                    seed=seed,
                                    batch_words=batch_words
                             )  

model.save('word2vec.model')
models = word2vec.Word2Vec.load('word2vec.model')
#print(models.wv['endometriosis'].shape)
#print(models.wv.most_similar(key,topn=top))
print('SG')
print(models.wv.most_similar(key,topn=top))
'''for item in models.wv.similar_by_word(key, top):
    print(item[0])'''
print("【顯示詞語】")
#print(models.wv.index_to_key)
key=models.wv.index_to_key
print(key[0:top])
# 显示词向量矩阵
#print("【词向量矩阵】")
#vectors = models.wv.vectors
# 提取词向量
#vectors = [models.wv[word] for word in models.wv.index_to_key]
vectors = [models.wv[word] for word in key[:]]
#print(len(model.wv.index2word))
#print(vectors)
#print(vectors.shape)
# 显示四个词语最相关的相似度
'''print("【词向量相似度】")
for i in range(top):
    print(models.wv.similar_by_vector(vectors[i]))'''
# 基于KMeans聚类
labels = KMeans(n_clusters=4).fit(vectors).labels_
#print(labels)

matplotlib.rcParams['axes.unicode_minus'] = False    # 显示负号
fig = plt.figure()
ax = mplot3d.Axes3D(fig)                             # 创建3d坐标轴
colors = ['red', 'blue', 'green','black']
# 绘制散点图 词语 词向量 类标(颜色)
for word, vector, label in zip(key[0:top], vectors, labels):
    ax.scatter(vector[0], vector[1], vector[2], c=colors[label], s=500, alpha=0.4)
    ax.text(vector[0], vector[1], vector[2], word, ha='center', va='center')
    #adjustText.adjust_text(texts)
plt.show()

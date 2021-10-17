import os
import xml.etree.ElementTree as ET
import json
import nltk
import re
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize


path = str(input("請輸入路徑:"))
print(path)
txt = str(input("請輸入欲搜尋文字:"))
print("您要找的文字是"+txt) 
try:
    file = open(path, 'r')
except FileNotFoundError:
    print(path + '不存在')
except PermissionError:
    print(path + '不是檔案')
else:
    #print(path + '檔案存在')
    file.close()
nm = os.path.splitext(path)
#folder=os.path.dirname(path)
#fnm=os.path.basename(path).split('.')
#print("folder:"+folder+"~fnm:"+fnm[0])
#newfile = Path(folder+'/'+fnm[0]+'.txt')
#newfile.touch(exist_ok=True)
#f = open(newfile,'w',encoding="utf-8")
#f.write("test1\n")
str1=""
if nm[1]==".xml":
    #print("您輸入xml")
    # 從檔案載入並解析 XML 資料
    tree = ET.parse(path)
    root = tree.getroot()
    #print(root.tag)
    ## 搜尋所有子節點
    for AbstractText in root.iter('AbstractText'):
        #syn = str(AbstractText.text).synsets(txt)
        #print(syn[0].examples())
        #print(AbstractText.text)
        str1=str1+AbstractText.text
'''elif nm[1]==".json":
    #print("您輸入json")
    # 將 json 檔案讀取成字串
    json_data = open(path,"r",encoding="utf-8").read()
    # 對json資料解碼
    data = json.loads(json_data)
    # 直接列印 data
    for i in range(len(data)):
        #print(data[i]['tweet_text'])
        str1=str1+data[i]['tweet_text']'''
        #f.write(data[i]['tweet_text']+"\n")
    #syn = str(str1).synsets(txt)
    #print(syn[0].examples())
#print(str1)

    
mark_out = re.sub(r'[^\w\s]','',str1.replace('/', ' '))

sentences = sent_tokenize(str1)
words=word_tokenize(mark_out)
characters=str(len(mark_out))
    #print(sentences)
print(path)    
print('Number of sentences by nltk: ' + str(len(sentences)))
print('Number of words by nltk: ' + str(len(words)))
print('Number of characters: ' + characters)
'''for i in range(len(words)):
    print(words[i]+"\n")'''

for i in range(len(sentences)):
   if txt in sentences[i]:
        print(sentences[i]+"\n")
'''with open(newfile) as file:
    for line in file:
        print(line.rstrip())'''
import os,sys
import nltk
import re
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize

path=['','']
file=['','']
nm=['','']
string=['','']
sentences=[0,0]
words=[0,0]
characters=[0,0]
for i in range(len(path)):
    path[i] = str(input("請輸入第"+str(i+1)+"份文件路徑:"))
    #print(path[i])

    try:
        file[i] = open(path[i], 'r')
    except FileNotFoundError:
        print(path[i] + '不存在')
        sys.exit(1)
    except PermissionError:
        print(path[i] + '不是檔案')
        sys.exit(1)
    else:
        #print(path + '檔案存在')
        #file[i].close()
        nm[i] = os.path.splitext(path[i])
#folder=os.path.dirname(path)
#fnm=os.path.basename(path).split('.')
#print("folder:"+folder+"~fnm:"+fnm[0])
#newfile = Path(folder+'/'+fnm[0]+'.txt')
#newfile.touch(exist_ok=True)
#f = open(newfile,'w',encoding="utf-8")
#f.write("test1\n")

        if nm[i][1]==".txt":
            string[i]=file[i].read()
            file[i].close()
            mark_out = re.sub(r'[^\w\s]','',string[i].replace('/', ' '))
            
            sentence = sent_tokenize(string[i])
            word=word_tokenize(mark_out)
            characters[i]=str(len(mark_out.replace(' ','')))
            sentences[i]=len(sentence)
            words[i]=len(word)
            #words[i]=[len(word),word]
            print(words[i])
                #print(sentences)
            #print(path)    
            print('Number of sentences by nltk: ' + str(sentences[i]))
            print('Number of words by nltk: ' + str(words[i]))
            print('Number of characters: ' + characters[i])
'''for i in range(len(words)):
    print(words[i]+"\n")'''
if(sentences[0]==sentences[1]):
    if(words[0]==words[1]):
        if(characters[0]==characters[1]):
            if string[0] in string[1]:
                print("文章相同")
            else:
                print("文章內容不同")
        else:
            print("文章字元不同")
    else:
        print("文章字數不同")
else:
    print("文章句子不同")



# -*- coding: utf-8 -*-
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
keyword = 'Endometriosis'
for i in range(500):
    
    link="https://pubmed.ncbi.nlm.nih.gov/?term="+ str(keyword) +"&filter=years.2013-2021&format=abstract&page="+str(i+1)
    #print(link)

    response = session.get(link)
    #print(response.html.text)
    soup = BeautifulSoup(response.text, "html.parser")
    #elements = soup.select("div.abstract-content.selected p")#取HTML標中的 <div class="abstract-content.selected"></div> 中的<p>標籤存入sel
    #elements = soup.find_all("div", class_="abstract-content.selected")
    elements = soup.find_all("div", class_="abstract")
    #print(result)
    #getkeywords=soup.select("strong.sub-title p")
    #print(soup.prettify())
    #result = soup.find_all(["p"])
    #print(elements)
    count=0
    #for getkeyword in getkeywords:
        #print(getkeyword.text)
    for element in elements:
        count+=1
        #print('count'+str(count))
        em= element.select_one("em")
        #print(em)
        if em is None :
            filename = 'Endometriosis_' + str(i+1)+'_'+str(count) +'.txt' 
    
            f = open(filename, 'a', encoding='UTF-8')
            #title = element.select_one("p").getText()
            #title = element.find_all("p").getText().strip()
            title = element.find_all("p")
            for j in range(len(title)):
                #print(str(i)+":"+title[j].text)
                f.write(title[j].text)
        else:
            "No Description"
        f.close()
        
         #title = element.select_one("p").text
        #print("len:"+str(len(title)))
        #print(element.text)
        '''filename = 'Endometriosis_' + str(i+1)+'_'+str(count) +'.txt' 
    
        f = open(filename, 'a', encoding='UTF-8')    

        f.write(element.text)
        
        f.close()'''
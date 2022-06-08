#!/usr/bin/python3
import time,random, sys, os
from bs4 import BeautifulSoup as bs
import requests as rq
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, XLNetLMHeadModel, XLNetTokenizer, pipeline


def affichage_temps_restant(temps_restant):
    cmpt_heure=0
    cmpt_minute=0
    while temps_restant != 0:
        if temps_restant >= 3600 : # 1 heure en secondes
            temps_restant=temps_restant-3600
            cmpt_heure=cmpt_heure+1
        elif temps_restant >= 60 : # 1 minute en secondes
            temps_restant=temps_restant-60
            cmpt_minute=cmpt_minute+1
        else: # le temps restant est < 1 min
            break
        #endif
    #endwhile 
    print("\ninfo: temps d'éxécution "+str(cmpt_heure)+" Heure(s) "+str(cmpt_minute)+ " Minute(s) "+str(round(temps_restant))+ " Seconde(s)" )
#endef

def requeteHTTP(base_url):
    url=base_url
    headers = {
	'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    }
    r = rq.get(url,headers=headers)
    #r = rq.get(url)
    soup = bs(r.content, 'html.parser')
    #print("url:"+str(url))
    #print (soup)
    return soup
#endef

def parse_next_url(soup,base_url):
    a=soup.find(class_='nextChapter')
    b=str(a).split(" ")
    c=b[2].split("=")
    if c[0] == "disabled\"":
        return base_url
    else:
        next_url=c[1].replace("\"","")   
        return next_url
#endef

def parse_book_title(soup):
    ol= soup.find('ol', {'class': 'breadcrumb'})
    children = ol.findChildren("li" , recursive=False)
    data=children[1].find('span')
    return data.text
#endef

def parse_chapter_title(soup):
    ol= soup.find('ol', {'class': 'breadcrumb'})
    children = ol.findChildren("li" , recursive=False)
    data=children[2].find('span')
    return data.text
#endef

def parse_chapter_content(soup,book_title):
    div = soup.find('div', {'class': 'chapter-content'})
    children = div.findChildren("p" , recursive=False)
    return children
#endef

def build_markdown(children,chapter_title):
    print("info: build markdown with original data")
    f = open("EN_"+str(book_title)+".md", "a")
    f.write("# "+str(chapter_title)+"\n\n\n")
    for child in children:
        f.write(child.text+"\n\n\n\n\n")
    f.close()
#endef

def translate_in_french_and_build_markdown(tokenizer,model,children,book_title,chapter_title,device):
    print("info: translate english to french and build markdown")
    f = open("FR_"+str(book_title)+".md", "a")
    input_ids= tokenizer(book_title , return_tensors="pt").to(device)
    model=model.to(device)
    outputs = model(**input_ids)
    result=tokenizer.batch_decode(outputs, skip_special_tokens=True)
    f.write("# "+str(result[0])+"\n\n\n")

    for child in children:
        data=str(child.text)
        ref=len(data)
        j=0
        actual_point=0
        next_point=1
        while ref > 0:
            if ref > 500:
                ref=ref-500
                for i in range(500*(j+1),actual_point,-1):
                    if data[i] == ".":
                        if j == 0:
                            actual_point=0
                            next_point=i
                        elif actual_point != next_point :
                            actual_point=next_point
                            next_point=i
                            break
                        #endif
                    #endif
                #endfor
                if j==0:
                    data_split=data[0:next_point+1]
                else:
                    data_split=data[actual_point+1:next_point+1]
                #endif
                input_ids= tokenizer(data_split , return_tensors="pt").to(device)
                model=model.to(device)
                outputs = model(**input_ids)
                result=tokenizer.batch_decode(outputs, skip_special_tokens=True)
                f.write(result[0])
                j=j+1
                
                if ref <= 500:
                    actual_point=next_point
                    for i in range(len(data)-1,actual_point,-1):
                        if data[i] == ".":
                            next_point=i
                            break
                        #endif
                    #endfor

                    ref=0
                    data_split=data[actual_point+1:]
                    input_ids= tokenizer(data_split , return_tensors="pt").to(device)
                    model=model.to(device)
                    outputs = model(**input_ids)
                    result=tokenizer.batch_decode(outputs, skip_special_tokens=True)
                    # print("trad=\n"+str(result[0]))
                    f.write(result[0]+"\n\n\n\n\n")
                    j=j+1
                #endif
            elif ref <= 500 and j == 0:
                ref=0
                input_ids= tokenizer(data , return_tensors="pt").to(device)
                model=model.to(device)
                outputs = model(**input_ids)
                result=tokenizer.batch_decode(outputs, skip_special_tokens=True)
                f.write(result[0]+"\n\n\n\n\n")
                j=j+1
             #endif
    f.close()

def generate_file(book_title):
    print("info: generate "+str(book_title)+".epub")
    cmd="pandoc -f markdown --toc --toc-depth=1  --epub-cover-image=epub-conf/cover.png --css=epub-conf/book.css  -o 'FR_"+str(book_title)+".epub' 'FR_"+str(book_title)+".md'"
    try:
        os.system(cmd)
    except:
        pass 
#endef

def check_args():
    # arg is present
    if len (sys.argv) < 2:
        print("error: You must specified an URL to scrap\nexample:\npython3 teenfic-scraper.py https://teenfic.net/the-serpentine-of-slytherin-draco-malfoy-completed-a-little-backstory-797249847.html ")
        sys.exit(1)
    #endif
    # arg is a valid url
    if "https://teenfic.net" in sys.argv[1]:
        pass
    else:
        print("error: Invalid URL")
        sys.exit(1)
    #endif
    return sys.argv[1]
#endef
 
def clean_file(book_title):
    print("info: remove old markdown files")
    cmd="rm 'FR_"+str(book_title)+"'.md"
    try:
        os.system(cmd)
    except:
        pass
#endef


if __name__ == '__main__' :
    torch.cuda.is_available()
    random.seed()
    start = time.time()

    # model init
    device = "cuda:0" if torch.cuda.is_available() else "cpu" # use GPU if CUDA is available
    model_name = "Helsinki-NLP/opus-mt-tc-big-en-fr" 
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    i=0
    while True:
        if i == 0:
            base_url=check_args()
        else:
            next_url=parse_next_url(soup,base_url)
            if next_url != base_url:
                base_url=next_url
            else: 
                break #end scraping
            #endif
        #endif
        soup=requeteHTTP(base_url)
        book_title=parse_book_title(soup)
        chapter_title=parse_chapter_title(soup)
        if i == 0:
            clean_file(book_title)
        #endif
        print("info: web scraping "+str(book_title)+" "+str(chapter_title))
        children=parse_chapter_content(soup,book_title)
        translate_in_french_and_build_markdown(tokenizer,model,children,book_title,chapter_title,device)
        i=i+1
    #endwhile
    print("info: web scraping done")
    generate_file(book_title)
    end = time.time()
    temps_restant=end-start
    affichage_temps_restant(temps_restant)
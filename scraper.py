#!/usr/bin/python3
import time,random
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests as rq
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# pip install bs4 pandas requests pytorch sentencepiece sacremoses torch

def requeteHTTP(base_url):
    #url='https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui='+profession+'&ou='+localisation+'&univers=pagesjaunes&page='+str(page)
    url=base_url
    headers = {
	'Connection':'keep-alive',
    'Host': 'www.pagesjaunes.fr',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }
    r = rq.get(url,headers=headers)
    #r = rq.get(url)
    soup = bs(r.content, 'html.parser')
    #print("url:"+str(url))
    #print (soup)
    return soup
#endef

def parser_prenom(id_modif):

    k=id_modif.find(' ')
    """
    print("emplacement espace="+str(k))
    print("id_modif="+id_modif)
    """
    prenom=id_modif[0:k]

    # vérification du prénom
    if prenom == "Dr":
        prenom_tmp=id_modif[k+1:len(id_modif)]
        #print("prenom_tmp:"+prenom_tmp)
        l=prenom_tmp.find(' ')
        #print("l:"+str(l))
        prenom=prenom_tmp[0:l]
    #endif
    return prenom
#endef

if __name__ == '__main__' :
    start = time.time()
    # initialisation graine random
    random.seed()

    # base_url="https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui="
    # soup=requeteHTTP(base_url)
    # id=soup.find_all('h3',{'class': 'company-name noTrad'})
    # adresse=soup.find_all(class_='adresse-container noTrad')


    # Define the model repo
    model_name = "Helsinki-NLP/opus-mt-en-fr" 

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    inp = "Hello, I'am Marc"
    input_ids = tokenizer(inp, return_tensors="pt").input_ids
    outputs = model.generate(input_ids=input_ids)
    result=tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print(result[0])
    #print("Generated:", tokenizer.batch_decode(outputs, skip_special_tokens=True))

    end = time.time()
    temps_restant=end-start
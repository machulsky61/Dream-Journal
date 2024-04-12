# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer=WordNetLemmatizer()
import pickle
import time
import random
import pickle

random.seed(a=None)


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

fail = []
data = pd.DataFrame() # diccionario indexado por exp_id con la data del reporte



for pagenum in np.arange(1400,1500):
    

    
    r = requests.get('http://www.dreamjournal.net/main/results?page='+str(pagenum))  # define la pagina
 
    reports = r.text.split('href="/journal/dream/dream_id/')  # particiona por reportes

    print(len(reports)-1)
         
    for n in np.arange(2,len(reports)-1): 
    
    
            print("Pagina numero:")
            print(pagenum)
            print("Reporte numero:")          
            print(n-1)
            
            
                
            temp = reports[n].split('/username/')
            id_val = temp[0]
            user_val = temp[1].split('">')[0]
                
            
                
            url_val = 'http://www.dreamjournal.net/journal/dream/dream_id/'+id_val+'/username/'+user_val
            time.sleep(5*random.random())
  
            try:             
                                        
                r2 = requests.get(url_val)  
                # get cohesion, rating, lucidity
                split1 = r2.text.split('>Rating')
                if len(split1) > 1:
                    rating = int(split1[1].split('%')[0].split(':')[1])/20
                else:
                    rating = -1
                
                split1 = r2.text.split('>Cohesion')
                if len(split1) > 1:
                    cohesion = int(split1[1].split('%')[0].split(':')[1])/20
                else:
                    cohesion = -1
                    
                split1 = r2.text.split('>Lucidity')
                if len(split1) > 1:
                    lucidity = int(split1[1].split('%')[0].split(':')[1])/20
                else:
                    lucidity = -1
                    
                split1 = r2.text.split('<br>Technique:')
                if len(split1) > 1:
                    technique = split1[1].split('\r\n')[0].replace(" ", "")
                else:
                    technique = '-1'
                    
                split1 = r2.text.split('Intent')
                if len(split1) > 1:
                    intent = split1[1].split('color:')[1].split(';')[0]
                else:
                    intent = '-1'
                
                text = cleanhtml(r2.text.split('post-desc">')[1].split('<b>Keywords</b>')[0])
                text = re.sub('\W+',' ', text)            # remueve \*
                text = re.sub(r'\d+', '', text).lower()   # remueve puntuacion  
                    
                tokens=word_tokenize(text)
                tipo=nltk.pos_tag(tokens) #clasifica que tipo de palabra es
                roots=[]
                for m in np.arange(0,len(tipo)): #traduce los tag al tag usado en lemmatize
                    if tipo[m][1][0]=='V':
                        tag='v'
                    elif tipo[m][1][0]=='J':
                        tag='a'
                    elif tipo[m][1][0]=='R' and tipo[m][1][1]=='B':
                        tag='r'
                    else:
                        tag='n'
                    roots.append(wordnet_lemmatizer.lemmatize(tipo[m][0],pos=tag))
                roots=remove_values_from_list(roots,'nbsp')
                    
                data=data.append({'id':id_val, 'user':user_val, 'url':url_val, 'text':text, 'raices':roots, 'rating':rating, 'cohesion':cohesion, 'lucidity':lucidity, 'intent':intent, 'technique':technique}, ignore_index=True)
            
            except:
                print('error')
                fail.append(url_val)
                
with open(r'C:\Users\Z420\Documents\analisis_semantico\dreamjournal\data7.pickle', "wb") as output_file:
    pickle.dump(data,output_file)





fail = []
data = pd.DataFrame() # diccionario indexado por exp_id con la data del reporte





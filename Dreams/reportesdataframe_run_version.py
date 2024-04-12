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
random.seed(a=None)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


#data = pd.DataFrame()
data = pickle.load( open( "C:\Users\users\Documents\work\erowid\dataframe_reducido.p", "rb" ) )
fail = pickle.load( open( "C:\Users\users\Documents\work\erowid/fails.p", "rb" ) )

#fail=[]


#ids= [39, 1, 44, 3, 2, 695, 22, 207, 61, 13, 76, 172, 38, 6, 18, 31, 37, 45, 58, 539, 26, 137, 396, 57, 10, 41, 203, 15, 40, 7, 52, 109, 149, 176, 54, 11, 27, 8, 111, 21, 5, 17, 143, 30, 25, 527, 64, 14, 484, 53, 98, 198, 47, 74, 628, 114, 472, 199, 255, 266, 87, 265, 387, 191, 217, 104, 148, 284, 34, 377, 458, 94, 183, 99, 97, 125, 138, 262, 166, 93, 43, 48, 105, 483, 273, 115, 211, 107, 68, 69, 84, 113, 95, 223, 169, 88, 89, 196, 96, 119, 139, 357, 23, 82, 110, 305, 321, 287, 342, 179, 101, 63, 103, 516, 51, 121, 186, 276, 281, 682, 267, 79, 19, 55, 131, 153, 36, 90, 300, 188, 603, 150, 349, 311, 282, 499, 106, 170, 259, 285, 304, 80, 200, 563, 9, 28, 272, 42, 142, 165, 294, 221, 67, 151, 568, 20, 312, 558, 100, 216, 227, 260, 379, 173, 348, 92, 112, 316, 210, 185, 274, 290, 133, 193, 350, 389, 209, 134, 408, 190, 244, 346, 280, 291, 386, 65, 286, 365, 239, 388, 250, 167]
ids=   [190, 244, 346, 280, 291, 386, 65, 286, 365, 239, 388, 250, 167]
numero=[1946, 1850, 1671, 1534, 1420, 1104, 701, 669, 546, 540, 494, 482, 480, 460, 421, 364, 350, 348, 343, 331, 329, 329, 320, 310, 304, 299, 299, 295, 294, 290, 286, 260, 255, 248, 236, 227, 226, 222, 217, 213, 212, 206, 191, 184, 181, 181, 176, 174, 167, 166, 156, 150, 148, 147, 147, 145, 144, 141, 138, 137, 135, 135, 133, 130, 130, 124, 124, 123, 115, 108, 108, 107, 106, 104, 103, 101, 101, 100, 98, 96, 95, 95, 92, 90, 89, 88, 84, 83, 82, 82, 81, 80, 79, 79, 78, 75, 75, 75, 73, 73, 73, 73, 71, 69, 69, 69, 68, 67, 66, 65, 63, 62, 62, 62, 59, 59, 59, 59, 59, 59, 57, 56, 55, 55, 53, 53, 52, 52, 52, 51, 51, 49, 46, 45, 44, 44, 43, 43, 43, 43, 43, 42, 42, 42, 40, 40, 40, 37, 37, 37, 37, 35, 34, 34, 34, 33, 33, 33, 32, 32, 32, 31, 30, 29, 29, 28, 28, 25, 24, 23, 23, 22, 21, 21, 21, 21, 20, 19, 19, 17, 17, 17, 16, 16, 16, 15, 15, 13, 11, 11, 10, 7]

l=179


for i in ids:
    l=l+1
    print l
    print numero[l-1]
    time.sleep(5*random.random())
    r = requests.get('https://erowid.org/experiences/exp.cgi?S1='+str(i)+'&ShowViews=0&Cellar=0&Start=0&Max=10000')  # define la sustancia
    
    reports = r.text.split('href="exp.php?ID=')  # particiona por reportes
        
    print (l)
    for n in np.arange(1,numero[l-1]+1):  
             
        print n
        
        try:
    
            drugs = reports[n].split('</a></td>')[1].split('</td><td>')[1].split('</td><td')[0]
            exp_id = reports[n].split('</a></td>')[0].split('">')[0]
            title = reports[n].split('</a></td>')[0].split('">')[1]
        
            url_report = 'https://erowid.org/experiences/exp.php?ID=' + exp_id
            r = requests.get(url_report)
            #aca hay que agregar un if que sea: si no existe star body en la pag pasa a la siguiente
            report = cleanhtml(r.text.split('-- Start Body -->')[1].split('<!-- End Body -->')[0])
            report = re.sub('\W+',' ', report)            # remueve \*
            report = re.sub(r'\d+', '', report).lower()   # remueve puntuacion
            tokens=word_tokenize(report)
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
            data=data.append({'titulo':title, 'droga':drugs, 'reporte':report, 'raices':roots, 'exp':exp_id}, ignore_index=True)
            
        except:
            print 'error'
            url_report = 'https://erowid.org/experiences/exp.php?ID=' + exp_id
            fail.append('https://erowid.org/experiences/exp.php?ID=' + exp_id)

           
        
pickle.dump( data, open( "C:\Users\users\Documents\work\erowid\dataframe.p", "wb" ) )
pickle.dump( fail_data, open( "C:\Users\users\Documents\work\erowid/fail_data.p", "wb" ) )
pickle.dump( data, open( "C:\Users\users\Documents\work\erowid\drug_data.p", "wb" ) )

data=data.set_index('exp')
#data.to_pickle('datos.p')
#pickle.dump(fail, open( 'fallos.p', 'wb' ))
#para abrir los datos: pd.read_pickle('datos.p')
#para abrir los fallos: fallos=pickle.load(open( 'fallos.p', 'rb' ))


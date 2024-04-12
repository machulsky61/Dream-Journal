import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=1)

corpus = []

for i in data['raices'].index:
    print len(data['raices'].index)-i
    corpus.append(' '.join(data['raices'][i]))

X = vectorizer.fit_transform(corpus).toarray()

def frequency_matrices(data, label_list,minpercentage, maxpercentage):
    all_words = []
    total_reports = 0
    used_drugs = []
    used_words = []
    
    for d,drug in enumerate(label_list):
            all_reports = data['raices'][data['droga']==drug]
            for report in enumerate(all_reports):
                used_drugs.append(drug) 

    
    for drug in label_list:  # obtain all the words that appear in the report collection
        print drug
        total_reports = total_reports + len(data['raices'][data['droga']==drug])
        words = list(set().union(*list(data['raices'][data['droga']==drug])))
        all_words= list(set().union(words,all_words))
        
    count_matrix = np.empty([0, total_reports])
    for w,word in enumerate(all_words):   # iterate across all words and reports and get the count of each word in the report
        r = -1
        temp = np.zeros(total_reports)
        print len(all_words)-w, word
        for d,drug in enumerate(label_list):
            all_reports = data['raices'][data['droga']==drug]
            for report in enumerate(all_reports):
                r = r + 1
                temp[r] = report[1].count(word)

        if 100*sum(temp>0)/r > minpercentage and 100*sum(temp>0)/r < maxpercentage:
            print('ok!')
            count_matrix = np.vstack([count_matrix, temp])
            used_words.append(word)
                
    
    tf_idf_matrix = count_matrix       # applies TF-IDF normalization
    for w,word in enumerate(used_words):
        print w,word
        
        tf_idf_matrix[w,:] = tf_idf_matrix[w,:]*np.log(total_reports/sum(count_matrix[w,:]>0))
        
    
    return [count_matrix, tf_idf_matrix, used_words, used_drugs]
            
    ### aplica SVD para tener LSA
nd = 8
freq_matrix = results[1]       
U, s, V = np.linalg.svd(freq_matrix, full_matrices=True)        
Ubis = U[:,0:nd]     
Vbis = V[0:nd, :]
S = np.zeros((nd, nd))
S[:nd, :nd] = np.diag(s[0:nd])
freq_low_rank = np.dot(Ubis, np.dot(S, Vbis))
correlacion = np.corrcoef(np.transpose(freq_low_rank))


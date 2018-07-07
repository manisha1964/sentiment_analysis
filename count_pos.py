import string,re, sys, nltk, json, csv, codecs
from string import punctuation
import heuristics as h
from os import listdir
from nltk.corpus import stopwords, sentiwordnet as swn, wordnet as wn
from itertools import groupby
#from spellcheck import spellCheck
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from collections import Counter
sia = SIA()
stop_words = set(stopwords.words('english'))
vader_dict={}
#s = SentiWordNetCorpusReader("../nltk_data/corpora/sentiwordnet", ["SentiWordNet_3.0.0_20130122.txt"])
#spch=spellCheck()
#['__HNDL', '__URL', 'Aww', 'thats', 'a', 'bummer', 'You', 'shoulda', 'got', 'David', 'Carr', 'of', 'Third', 'Day', 'to', 'do', 'it', '__EMOT_WINK']
def map_emoji_to_rating(word):
    if word == '__EMOT_SMILEY' or word == '__EMOT_LOVE' or word == '__EMOT_WINK':
        return 2
    if word == '__EMOT_LAUGH':
        return 1
    if word == '__EMOT_FROWN':
        return 3
    if word == '__EMOT_CRY':
        return 4

def vader(word):
    try:
        return vader_dict[word]
    except KeyError:
        try:
            return sia.polarity_scores(word)['compound']
        except KeyError:
            return False

def sentiword(word, tagged):
    for item in tagged:
        if item[0] == word:
            tag=item[1]
    #print word, tag
    sen_sets=wn.synsets(word,pos=h.POS_LIST.get(tag))
    #print sen_sets
    if not sen_sets:
        return 0.0
    #print 'synonym score'
    try:
        a = swn.senti_synset(sen_sets[0].name())
    except:
        return 0.0
    pos,neg = a.pos_score(),a.neg_score()
    #print pos, neg
    if pos>=neg:
        return a.pos_score()
    else:
        return -a.neg_score()



def findpolarity(rem, tagged):
    #['she', 'sed', 'puerto', 'rican']
    polarity={}
    for word in rem:
        if h.polarity_list.has_key(word):
            polarity[word]=h.polarity_list[word]
            #print polarity[word]
        elif h.polar_lookup.has_key(word):
            polarity[word]=h.polar_lookup[word]
        elif vader(word):
            vader_dict[word]=vader(word)
            polarity[word]=vader_dict[word]
        try:
            if polarity[word] == 0.0:
                polarity[word]=sentiword(word, tagged)
        except KeyError:
            polarity[word]=sentiword(word, tagged)
    return polarity


def feature_extraction(tokens, tagged, polar, l1):
    global cntt
    pos_dict={}
    #print cntt, 'fext'
    for item in tagged:
        pos_dict[item[0]]=item[1]
    for item in tokens:
        #print pos_dict[item], polar[item]
        if 'NN' in pos_dict[item]:
            if polar[item] > 0.0:
                l[cntt][l1]+=1.0
            elif polar[item] < 0.0:
                l[cntt][l1+1]+=1.0
            else:
                l[cntt][l1+2]+=1.0
        elif 'JJ' in pos_dict[item]:
            if polar[item] > 0.0:
                l[cntt][l1+3]+=1.0
            elif polar[item] < 0.0:
                l[cntt][l1+4]+=1.0
            else:
                l[cntt][l1+5]+=1.0
        elif 'RB' in pos_dict[item]:
            if polar[item] > 0.0:
                l[cntt][l1+6]+=1.0
            elif polar[item] < 0.0:
                l[cntt][l1+7]+=1.0
            else:
                l[cntt][l1+8]+=1.0
        elif 'VB' in pos_dict[item]:
            if polar[item] > 0.0:
                l[cntt][l1+9]+=1.0
            elif polar[item] < 0.0:
                l[cntt][l1+10]+=1.0
            else:
                l[cntt][l1+11]+=1.0
        else:
            if polar[item] > 0.0:
                l[cntt][l1+12]+=1.0
            else:
                l[cntt][l1+13]+=1.0

def feature_sum(tokens, tagged, polar, l2):
    nn=0.0
    jj=0.0
    rb=0.0
    vb=0.0
    total=0.0
    global cntt
    #print cntt, 'feature_sum'
    pos_dict={}
    for item in tagged:
        pos_dict[item[0]]=item[1]
    for item in tokens:
        polar[item]=float(polar[item])
        if 'NN' in pos_dict[item]:
            nn=nn+polar[item]
        elif 'JJ' in pos_dict[item]:
            jj=jj+polar[item]
        elif 'RB' in pos_dict[item]:
            rb=rb+polar[item]
        elif 'VB' in pos_dict[item]:
            vb=vb+polar[item]
        else:
            total=total+polar[item]
    total=total+nn+jj+rb+vb
    l[cntt][l2]+=nn
    l[cntt][l2+1]+=jj
    l[cntt][l2+2]+=vb
    l[cntt][l2+3]+=rb
    l[cntt][l2+4]+=total
    
def spellingcheck(tokens):
    rem=[]
    for item in tokens:
        item=item.lower()
        #a=spch.correct(item)
        print item, a
        rem.append(a)
    return rem

def acronymapping(tokens):
    final=[]
    for item in tokens:
        if h.acronym_dict.has_key(item.lower()):
            final.extend(h.acronym_dict[item].split())
        else:
            final.extend(item.split())
    #print final
    return final

def process_hashtags(word):
    str="__HASH_"
    word=string.replace(word, str, "")
    word=word.lower()
    word=word.split()
    tagged=nltk.pos_tag(word)
    #print tagged
    polar=findpolarity(word, tagged)
    #print polar
    return polar

def clean_doc(doc):
    global cntt
    rettok=[]
    #print cntt, 'clean_doc'
    tokens=doc.split()
    rem=[]
    polar={}
    for word in tokens:
        #if not word.isalpha():
            #continue
        if word == '__PUNC_EXCL':
            l[cntt][11]+=1.0
        elif word == '__HNDL':
            l[cntt][0]+=1.0
        elif word == '__URL':
            l[cntt][2]+=1.0
        elif '__PUNC' in word:
            l[cntt][1]+=1.0
        elif '__HASH' in word:
            val=process_hashtags(word)
            if val > 0.0:
                l[cntt][3]+=1.0
            elif val < 0.0:
                l[cntt][4]+=1.0
            else:
                l[cntt][5]+=1.0
        elif word == '__NEG':
            l[cntt][6]+=1.0
        elif '__EMOT' in word:
            res = map_emoji_to_rating(word)
            l[cntt][res+6]+=1.0
        else:
            rem.append(word.lower())
    #rem=acronymapping(rem)
    #rem = spellingcheck(rem)
    #print rem
    tagged = nltk.pos_tag(rem)
    #Remove stop-words
    fl=[]
    for word in rem:
        if word in stop_words or not (word.isalpha()):
            continue
        else:
            fl.append(word)
    polar=findpolarity(fl, tagged)
    global glen
    global hlen
    feature_extraction(fl, tagged, polar, glen)
    feature_sum(fl, tagged, polar, hlen)
    #print l[cntt]
    #sys.exit()
    for item in tagged:
        # extracting all the POS namely ADJ, ADV, VERBS, NOUNS
        if 'JJ' in item[1] or 'RB' in item[1] or 'VB' in item[1] or 'NN' in item[1]:
            rettok.append(item[0])
    cntt+=1
    return rettok

#--------------------------------------------------------------------

keys=['handle', 'punc', 'url', 'phashtag', 'neghashtag', 'nhashtag', 'neg', '5e', '4e', '2e', '1e', 'excl']
polar_pos=['pNN', 'nNN', '0NN', 'pJJ', 'nJJ', '0JJ', 'pRB', 'nRB', '0RB', 'pVB', 'nVB', '0VB', 'pwords', 'nwords']
gsum=['NN_sum', 'JJ_sum', 'VB_sum', 'RB_sum', 'total_sum']

glen = len(keys)
keys.extend(polar_pos)
hlen = len(keys)
keys.extend(gsum)
#--------------------------------------------------------------------------

# cntt=0
# tweets=[]
# l=[[0.0]*len(keys) for i in range(49987)]
labels=[]
# vocab=Counter()
with open('train/data.csv', 'rb') as inp:
    reader=csv.reader(inp)
    for row in reader:
    	#vocab.update(clean_doc(row[2]))
        if row[1] == 'negative':
            labels.append(-1)
        elif row[1] == 'positive':
            labels.append(-1)
        elif row[1] == 'neutral':
            labels.append(0)
# print type(l), len(l), len(l[0])
# with open("train/senti.csv", "wb") as f:
#     writer = csv.writer(f)    
#     for row in l:
#         writer.writerow(row)

with open('train/labels.txt', 'wb') as op:
    json.dump(labels, op)
   
#print(vocab.most_common(600))
# min_occurane = 5

# tokens = [k for k,c in vocab.iteritems() if c >= min_occurane]
# print len(tokens)

# with open('train/vocab.txt', 'wb') as ip:
#     ip.write(json.dumps(tokens))

'''
with open('train/vocab.txt', 'rb') as ip:
	vocab=json.load(ip)
	
cntt=0
tweets=[]
l=[[0.0]*len(keys) for i in range(12284)]
with open('test/data.csv', 'rb') as inp:
    reader=csv.reader(inp)
    for row in reader:
        clean_doc(row[1])
print type(l), len(l), len(l[0])
with open("test/senti.csv", "wb") as f:
    writer = csv.writer(f)    
    for row in l:
        writer.writerow(row)
'''

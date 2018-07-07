import json, csv
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def clean_doc(doc):
    tokens = doc.split()
    #doc=doc.lower()
    rem=[]
    for word in tokens:
        if word == '__HNDL':
            pass
        elif word == '__URL':
            pass
        elif '__PUNC' in word:
            pass
        elif '__HASH' in word:
            pass
        elif word == '__NEG':
            pass
        elif '__EMOT' in word:
            pass
        else:
            rem.append(word)
    tokens=rem
    tokens = [word for word in tokens if word.isalpha()]
    #tokens = [w for w in tokens if w not in stop_words]
    #tokens = [word for word in tokens if len(word) > 1]
    return tokens


def doc_to_line(doc, vocab):
    tokens = clean_doc(doc)
    tokens = [w for w in tokens if w in vocab]
    return ' '.join(tokens)

def save_list(lines, filename):
    data = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()
    
def vectorize(st, corpus, vocab):
    vocab = list(set(vocab))
    print len(vocab)
    corpus = dict(((term, index) for index, term in enumerate(sorted(vocab))))
    num_words = len(corpus)
    senti=[]
    with open("%s/senti.csv" % st, "rb") as f:
        reader = csv.reader(f)    
        for row in reader:
            senti.append(row)
        print type(senti[0])
    with open('%s/tweets.txt' % st, 'r') as f:
        content = f.readlines()
        fvs = [[0]*num_words for x in range(len(content))]
    with open("%s/allfv.csv" % st, "wb") as f2:
        writer = csv.writer(f2)    
        for x in range(len(content)):
            fv = fvs[x]
            for word in content[x].split():
                fv[corpus[word]]+=1.0
            #print len(fv)
            fv.extend(senti[x])
            #print len(fv)
            writer.writerow(fv)
        

    
    
with open('train/vocab.txt', 'rb') as op:
   vocab=json.load(op)

trainlines=[]
testlines=[]
with open('train/data.csv', 'rb') as inp:
    reader=csv.reader(inp)
    for row in reader:
        trainlines.append(doc_to_line(row[2], vocab))
save_list(trainlines, 'train/tweets.txt')

with open('test/data.csv', 'rb') as inp:
    reader=csv.reader(inp)
    for row in reader:
        testlines.append(doc_to_line(row[1], vocab))
save_list(testlines, 'test/tweets.txt')

vectorize("train",trainlines, vocab)
vectorize("test",testlines, vocab)

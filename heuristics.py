import re, json, csv


NEGATE = ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
 "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
 "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
 "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
 "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
 "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
 "oughtn't", "shan't", "shouldn't", "uh-uh", "wasn't", "weren't",
 "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite", "would not",
  "could not", "has not", "had not", "have not", "are not", "is not", "am not", 
  "will not", "shall not", "ought not", "should not", "did not", "does not", "do not", "dare not", 
  "might not ", "must not ", "need not ", "can not ", "was not ", "were not ", "lack of"]
# load doc into memory
IN = ["extremely", "most", "really", "pretty", "extraordinarily", "slightly", "somewhat", "very", "atall", "at all", "too", "sorely", "barely", "little"]
CONJ = ["and", "but", "or"]
POS_LIST = {
    'VB': 'v',
    'VBD': 'v',
    'VBG': 'v',
    'VBN': 'v',
    'VBP': 'v',
    'VBZ': 'v',
    'JJ': 'a',
    'JJR': 'a',
    'JJS': 'a',
    'RB': 'r',
    'RBR': 'r',
    'RBS': 'r',
    'NN': 'n',
    'NNS': 'n',
    'NNPS': 'n',
    'NNP': 'n'
}
NEG_PATTERN = ["stop "+str(re.compile('[a-z]+ing$')), "quit "+str(re.compile('[a-z]+ing$'))]


polarity_list={}
with open('corpus/wordwithStrength.txt', 'rb') as file:
    polar=file.readlines()
    for item in polar:
        l = item.rstrip('\n').split('\t')
        polarity_list[l[0]]=l[1]

polar_lookup={}        
with open('corpus/SentimentLookupTable.txt', 'rb') as file:
    polar=file.readlines()
    for item in polar:
        l = item.rstrip('\n').split('\t')
        l[0]=l[0].replace('*', '')
        polar_lookup[l[0]]=float(l[1])/5.0
acronym_dict={}
with open('corpus/acronym.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        acronym_dict[row[0]]=row[1]

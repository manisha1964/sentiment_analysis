import os, csv

def make_Corpus(root_dir):
    polarity_dirs = [os.path.join(root_dir,f) for f in os.listdir(root_dir)]    
    corpus = []    
    with open('test/testdataset.csv', 'wb') as filew:
        writer=csv.writer(filew)
        all=[]
        label=[]
        cnt=0
        for polarity_dir in polarity_dirs:
            with open(polarity_dir, 'rb') as file:
                lines = file.readlines()
                for line in lines:
                    row=[]
                    line=line.rstrip('\n').split('\t')
                    #print line
                    row.append(cnt)
                    #print line[2], polarity_dir
                    row.append(line[2])
                    label.append(line[1])
                    all.append(row)
                    cnt+=1
        writer.writerows(all)
    with open('test/labels.txt', 'wb') as op:
        op.write('\n'.join(label))
    print len(label)
        


root_dir = 'gold'
corpus = make_Corpus(root_dir)

'''
reviews = [os.path.join(polarity_dir,f) for f in os.listdir(polarity_dir)]
            for review in reviews:
'''

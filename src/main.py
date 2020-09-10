"""
HW 1
Grade - 67/70
"""
### GET IMPORTS TO USE
import os
import string
import re
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from collections import OrderedDict
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
###use the following for string cleaning and pre processing
stoplist = stopwords.words('english')
stop_words = set(stopwords.words('english'))

### GET THE TRAINING AND TEST FILES AND ASSIGN A SHORTER NAME
training_file = open('1580506710_9392152_train_file.dat', 'r')
test_file = open('1580506710_9597683_test.dat', 'r')


## this returns the number of words which are same in positive reviews
def knnPos(str, word):
    ### the positive file is checked for word common
    ### given string is split in spaces
    each_word = str.split(" ")
    #start score from 0
    score = 0
    for i in range(0, len(each_word)):
        ###for 5 nearest neighbors
        if score < 5:
            if (word == each_word[i]):
                score = score + 1
    return score 

## this return the number of words which are same in negative reviews
def knnNeg(str, word):
    ### the negative file is checked for word common
    ### given string is split in spaces
    each_word = str.split(" ")
    #start score from 0
    score = 0
    for i in range(0, len(each_word)):
        ###for 5 nearest neighbors
        if score < 5:
            if (word == each_word[i]):
                score = score + 1
    return score 


## this will give a list with all unique words only.
## repeated words will be removed
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

###this will pre process the given string
def preProcess(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    processed = re.sub(r"\d+","",normalized)
    y = processed.split()
    return y

###########--------------------------------------------------

### get empty lists to put in the training data
positive = []
negative = []

### OPEN TRAINING DATA FILE
with training_file as tf:
    ### GET POSITIVE AND NEGATIVE REVIEWS AND SEPARATE THEM
    for line in tf:
        if line[0] == '+':
            positive.append(line)
        if line[0] == '-':
            negative.append(line)

### CREATE A SEPARATE FILE FOR POSITIVE AND NEGATIVE REVIEWS
with open("positiveOutputs.txt", "w") as txt_file:
    for line in positive:
        txt_file.write("".join(line))
        
with open("negativeOutputs.txt", "w") as txt_file:
    for line in negative:
        txt_file.write("".join(line))
###

#get all the positive reviews and remove stopwords
#then store in a separate file
file_p = open("positiveOutputs.txt") 
line_p = file_p.read()
line_p = preProcess(line_p)
for r in line_p: 
    if not r in stop_words:
        appendFile = open('positiveFilter.txt','a') 
        appendFile.write(" "+r) 
        appendFile.close()

    

#get all the negative reviews and remove stopwords
#then store in separate file    
file_n = open("negativeOutputs.txt") 
line_n = file_n.read()
line_n = preProcess(line_n)
for r in line_n: 
    if not r in stop_words:
        appendFile = open('negativeFilter.txt','a') 
        appendFile.write(" "+r) 
        appendFile.close()

    
### remove duplicates from the negative and positive filter files
negative_content = open('negativeFilter.txt','r').readline() 
positive_content = open('positiveFilter.txt','r').readline()


### remove duplicates from positive and negative filtered files 
positive_content=' '.join(unique_list(positive_content.split()))
negative_content=' '.join(unique_list(negative_content.split()))

file1 = open("positiveFilter.txt","w")
file1.write(positive_content)
file1.close()

file2 = open("negativeFilter.txt","w")
file2.write(negative_content) 
file2.close()

######
## now the positive and negative reviews are filtered
## stop words are eliminated cleaned
## now get testing data and implement KNN
#----------------------------- 
#----------------------------- 

positive_review_words = open('positiveFilter.txt','r').readline()
negative_review_words = open('negativeFilter.txt','r').readline()

score = []

###get each review from the test file
test_lines = tuple(test_file)

### start the reading from the test file line by line
for review in test_lines:
    ### defind positive and negative score for each review
    review_pos_score = 0
    review_neg_score = 0
    #get each word separated in each review
    review_clean = preProcess(review)
    #get each word from each inside the review review and implement KNN
    for word in review_clean:

        ### get positive and negative score of the review
        score_neg = knnNeg(negative_review_words, word)
        score_pos = knnPos(positive_review_words, word)
        ### increment the score for the positive and negative review
        review_pos_score = review_pos_score + score_pos 
        review_neg_score = review_neg_score + score_neg

    ### get the final score for the knn
    k_score = review_pos_score - review_neg_score
    if (k_score >= 0):
        score.append("+1")
    else:
        score.append("-1")

###FINALLY WRITE THE +1 -1 INTO THE FORMAT FILE
with open('format_file.txt', 'w') as filehandle:
    filehandle.writelines("%s\n" % place for place in score)

# clean unnecessary files created
os.remove("negativeOutputs.txt")
os.remove("positiveOutputs.txt")
os.remove("positiveFilter.txt")
os.remove("negativeFilter.txt")
    
##----------------------------- 
##    END
##----------------------------- 





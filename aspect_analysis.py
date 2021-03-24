# importing the python libraries to handle and process the text
import stanza   
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer 

# defining a function to perform aspect_analysis
def aspect_analysis(txt, stop_words, nlp):
    """this function is used to extract the aspects from the given text sentence with describing each aspect
        input :
                txt : the sentence from which the aspects have to be extracted
                stop_words : the list of unneccessary words to be removed from the given sentence
                nlp : a stanza pipeline to process, clean and so on etc, the sentence
        output : 
                a python dictionary with keys as aspect and values as description of aspects"""
    
    txt = txt.lower() # LowerCasing the given Text
    sentList = nltk.sent_tokenize(txt) # Splitting the text into sentences

    fcluster = []
    totalfeatureList = []
    finalcluster = []
    dic = {}

    for line in sentList:
        newtaggedList = []
        txt_list = nltk.word_tokenize(line) # Splitting up into words
        taggedList = nltk.pos_tag(txt_list) # Doing Part-of-Speech Tagging to each word

        # this part of code is to merge two worded nouns if any
        newwordList = []
        flag = 0
        for i in range(0,len(taggedList)-1):
            if(taggedList[i][1]=="NN" and taggedList[i+1][1]=="NN"): # If two consecutive words are Nouns then they are joined together
                newwordList.append(taggedList[i][0]+taggedList[i+1][0])
                flag=1
            else:
                if(flag==1):
                    flag=0
                    continue
                newwordList.append(taggedList[i][0])
                if(i==len(taggedList)-2):
                    newwordList.append(taggedList[i+1][0])

        finaltxt = ' '.join(word for word in newwordList) 
        new_txt_list = nltk.word_tokenize(finaltxt)
        wordsList = [w for w in new_txt_list if not w in stop_words]
        taggedList = nltk.pos_tag(wordsList)
        print(taggedList)
        doc = nlp(finaltxt) # Object of Stanford NLP Pipeleine
        
        # Getting the dependency relations between the words
        dep_node = []
        for dep_edge in doc.sentences[0].dependencies:
            dep_node.append([dep_edge[2].text, dep_edge[0].id, dep_edge[1]])

        # Coverting it into appropriate format
        for i in range(0, len(dep_node)):
            if (int(dep_node[i][1]) != 0):
                dep_node[i][1] = newwordList[(int(dep_node[i][1]) - 1)]

        featureList = []
        categories = []
        for i in taggedList:
            if(i[1]=='JJ' or i[1]=='NN' or i[1]=='JJR' or i[1]=='NNS' or i[1]=='RB'):
                featureList.append(list(i)) # For features for each sentence
                totalfeatureList.append(list(i)) # Stores the features of all the sentences in the text
                categories.append(i[0])
        # creating fcluster which holds every aspect centered cluster
        for i in featureList:
            filist = []
            for j in dep_node:
                if((j[0]==i[0] or j[1]==i[0]) and (j[2] in ["nsubj", "acl:relcl", "obj", "dobj", "agent", "advmod", "amod", "neg", "prep_of", "acomp", "xcomp", "compound"])):
                    if(j[0]==i[0]):
                        filist.append(j[1])
                    else:
                        filist.append(j[0])
            fcluster.append([i[0], filist])
            
    for i in totalfeatureList:
        dic[i[0]] = i[1]
    
    dicluster = {}
    for i in fcluster:
        dicluster[i[0]] = i[1]
    
    ## processing the fcluster to create the output dictionary
    nn_list=[]
    not_nn_list = []
    for i in dicluster:
        if nltk.pos_tag([i])[0][1] == "NN":
            nn_list.append(i)
        else:
            not_nn_list.append(i)
    key_list = nn_list+not_nn_list 
    
    # print("key_list",key_list,"nn",nn_list,"not",not_nn_list)
    
    findic = {}  
    for i in key_list:
        if nltk.pos_tag([i])[0][1] == "NN":
            findic[i] = dicluster[i][0]
        else:
            if len(dicluster[i])>1:
                temp = dicluster[i]
                print(temp)
                if nltk.pos_tag([temp[-2]])[0][1] == "NN":
                    print(f"{temp[-1]} {i}")
                    findic[temp[-2]] = f"{temp[-1]} {i}"
                     
    return(findic)
# nlp = stanza.Pipeline()
# stop_words = set(stopwords.words('english'))
# # txt = "The food is great but the service is very bad."
# txt = "the computer was goog but the screen was not bad"

# l = aspect_analysis(txt, stop_words, nlp)
# print(l[0],l[1],l[2],len(l),sep="\n")
# # print(nltk.pos_tag(["laptop"]))



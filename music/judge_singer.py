#coding=utf-8
'''
经过训练,分类器可以判断一首歌的演唱者是谁
'''
import jieba
import sklearn.feature_extraction
import sklearn.naive_bayes as nb
import sklearn.externals.joblib as jl
import os
import codecs
catedict = {
    u'汪峰':0,
    u'周杰伦':1,
    u'刀郎':2
}

gnb = nb.MultinomialNB(alpha = 0.01)
g_gnb = None
#Hashing Trick, transfrom dict -> vector
fh = sklearn.feature_extraction.FeatureHasher(n_features=15000,non_negative=True,input_type='string')

g_gnb = None

def predict(txt):
    global g_gnb
    kv = [t for t in jieba.cut(txt)]
    mt = fh.transform([kv])
    if g_gnb == None:
        g_gnb = jl.load('final2.pkl')
    num =  g_gnb.predict(mt)
    for (k,v) in catedict.viewitems():
        if(v==num):
            return k

def get_text_by_name(filename):
    file = codecs.open(filename,'r')
    text = file.read()
    return text

def judge_singer_by_nb_ex(dir):
    filenames = os.listdir(dir)
    for filename in filenames:
        if filename == '.DS_Store':
            continue
        name = os.path.join(dir,filename)
        text = get_text_by_name(name)
        singer = predict(text)
        print u'唱<<{name}>>的歌手是{singer}'.format(name=name,singer=singer)
def judge_singer_by_nb():
    judge_singer_by_nb_ex(u'./test/周杰伦')
    judge_singer_by_nb_ex(u'./test/汪峰')
    judge_singer_by_nb_ex(u'./test/刀郎')

def clipper(txt):
    return jieba.cut(txt)

def get_file_text(dir):
    text_lst = []
    filenames = os.listdir(dir)
    for filename in filenames:
        if filename == '.DS_Store':
            continue
        name = os.path.join(dir,filename)
        file = codecs.open(name,'r')
        text = file.read()
        text_lst.append(text)
    return text_lst
def train():
    kvlist = []
    targetlist = []
    zhou_lst = get_file_text('./周杰伦')
    wang_lst = get_file_text('./汪峰')
    dao_lst = get_file_text('./刀郎')
    for text in wang_lst:
        kvlist += [  [ i for i in clipper(text) ] ]
        targetlist += [0]

    for text in zhou_lst:
        kvlist += [  [ i for i in clipper(text) ] ]
        targetlist += [1]

    for text in dao_lst:
        kvlist += [  [ i for i in clipper(text) ] ]
        targetlist += [2]
    X = fh.fit_transform(kvlist)
    gnb.partial_fit(X,targetlist,classes = [i for i in catedict.viewvalues()])
    jl.dump(gnb,'final2.pkl')


if __name__ == '__main__':
    #train()
    judge_singer_by_nb()
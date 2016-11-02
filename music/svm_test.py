#coding=utf-8
import os

import jieba
import sklearn.feature_extraction
from sklearn import svm

import judge_singer

catedict = {
    u'汪峰':0,
    u'周杰伦':1,
    u'刀郎':2
}

fh = sklearn.feature_extraction.FeatureHasher(n_features=15000,non_negative=True,input_type='string')


def my_judge_singer(clf,dir):
    filenames = os.listdir(dir)
    for filename in filenames:
        if filename == '.DS_Store':
            continue
        name = os.path.join(dir,filename)
        text = judge_singer.get_text_by_name(name)
        kv = [t for t in jieba.cut(text)]
        mt = fh.transform([kv])
        num =  clf.predict(mt)
        for (k,v) in catedict.viewitems():
            if(v==num):
                print u'唱<<{name}>>的歌手是{singer}'.format(name=name,singer=k)

def test_by_kernel(kernel):
    if kernel:
        clf = svm.SVC(kernel=kernel)
    else:
        clf = svm.LinearSVC()
    kvlist = []
    targetlist = []
    zhou_lst = judge_singer.get_file_text('./周杰伦')
    wang_lst = judge_singer.get_file_text('./汪峰')
    dao_lst = judge_singer.get_file_text('./刀郎')
    for text in wang_lst:
        kvlist += [[i for i in judge_singer.clipper(text)]]
        targetlist += [0]

    for text in zhou_lst:
        kvlist += [[i for i in judge_singer.clipper(text)]]
        targetlist += [1]

    for text in dao_lst:
        kvlist += [[i for i in judge_singer.clipper(text)]]
        targetlist += [2]
    X = fh.fit_transform(kvlist)
    clf.fit(X,targetlist)
    my_judge_singer(clf,u'./test/刀郎')
    my_judge_singer(clf,u'./test/汪峰')
    my_judge_singer(clf,u'./test/周杰伦')
if __name__ == '__main__':
    test_by_kernel(None)
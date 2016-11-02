#coding=utf-8
import codecs
import os
def analyse_jielun():
    file = codecs.open(u'周杰伦歌词','r')
    lines = file.readlines()
    txtfile = None
    for line in lines:
        if line.startswith('|'):
            name = line.split('|')[1].replace('\n','')
            name = os.path.join('./周杰伦',name+'.txt')
            #name = u'./周杰伦/'+name+'.txt'
            print name
            if not txtfile == None:
                txtfile.close()
            txtfile = codecs.open(name,'w')
        else:
            if not txtfile == None:
                txtfile.write(line.strip()+'\r\n')
    txtfile.close()

def analyse_wangfeng():
    file = codecs.open(u'汪峰歌词.txt','r')
    lines = file.readlines()
    txtfile = None
    for line in lines:
        if line.startswith('!'):
            name = line.split('!')[1].replace('\n','')
            name = os.path.join('./汪峰',name+'.txt')
            #name = u'./周杰伦/'+name+'.txt'
            print name
            if not txtfile == None:
                txtfile.close()
            txtfile = codecs.open(name,'w')
        else:
            if not txtfile == None:
                txtfile.write(line.strip()+'\r\n')
    txtfile.close()

if __name__ == '__main__':
    analyse_wangfeng()


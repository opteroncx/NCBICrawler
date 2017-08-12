#-*-coding:utf8-*-
import requests
import re
import codecs
import threading as th
from bs4 import BeautifulSoup

head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}

def get_ID(keywords):
    #keywords= 'high+temperature+barley'
    data_id=requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%s&retmax=20000'%keywords,headers = head)
    ids=re.findall(r'<Id>(.*?)<',data_id.text,re.S)
    return ids

def extract_page(ids,num):
    #print 'start extract'
    #print len(ids)
    start=0
    end=0
    switcher={
             1:(0,len(ids)/4),2:((len(ids)/4)+1,len(ids)/2),3:((len(ids)/2)+1,len(ids)*3/4),4:((len(ids)*3/4)+1,len(ids))
              }
    (start,end)=switcher.get(num)
    i=start
    i=int(i)
    while(i<end):
        save = codecs.open('./archive/PMID%s.txt'%ids[i],'w','utf-8')
        info=requests.get('https://www.ncbi.nlm.nih.gov/pubmed/%s?report=xml&format=text'%ids[i],headers = head)
        #info_text=re.findall('<pre>(.*?)<',info.text,re.S)
        info_text=re.findall('AbstractText&gt;(.*?)&lt;',info.text,re.S)
        for line in info_text:
            save.writelines(line+'\n')
        try:
            ls=get_link(ids[i])
            save.writelines(ls+'\n')
        except Exception:
            print ('no link')
        save.close()
        print ('processing'+ids[i])
        i+=1
        
def multi_thread(ids):
    threads=[]
    t1=th.Thread(target=extract_page,args=(ids,1))
    threads.append(t1)
    t2=th.Thread(target=extract_page,args=(ids,2))
    threads.append(t2)
    t3=th.Thread(target=extract_page,args=(ids,3))
    threads.append(t3)
    t4=th.Thread(target=extract_page,args=(ids,4))
    threads.append(t4)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

def get_link(ids):
    html=requests.get('https://www.ncbi.nlm.nih.gov/pubmed/%s'%ids,headers = head)
    soup = BeautifulSoup(html.text)
    #print soup.find(class_="icons portlet")
    #print "####################"
    link_field=soup.find(class_="icons portlet")
    ls=link_field.find('a').get('href')
    #print type(link_field)
    #print type(ls)
    #print ls
    return ls
    
def run(keywords):
    print ('start')
    ids=get_ID(keywords)
    multi_thread(ids)

        
    
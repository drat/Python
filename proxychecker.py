#!/usr/bin/python

import time
import socket
import httplib
import urllib2
import threading
import Queue
import sys
import requests

TIMEOUT = 10

socket.setdefaulttimeout(TIMEOUT)

def check(host, port):
    try:
        proxy_handler = urllib2.ProxyHandler({'http': str(host)+":"+str(port)})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)
        req=urllib2.Request('http://www.wenti.de')  # change the URL to test here
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        return False
    except Exception, detail:
        print "Bad Proxy - "+host+":"+port
        return False
    with open('check.txt', 'a') as file:
      file.write(host+":"+port+"\n")
    return True

class CheckThread(threading.Thread):
    def __init__(self,no,q, r):
        threading.Thread.__init__(self)
        self.no = no
        self.q = q
        self.r = r

    def run(self):
        while True:
            proxy = []
            try:
                proxy = self.q.get(True,2)
            except:
                pass
            if len(proxy) == 0:
                break
            tstart = time.time()
            ret = check(proxy[0],proxy[1].replace("\n",""))
            tuse = time.time() - tstart
            if (ret) and tuse < TIMEOUT * 2:
                proxy.append(tuse)
                self.r.append(proxy)

class ProxyCheck:
    def __init__(self, tnum, file):
        self.tnum = tnum
        self.file = file

    def run(self, file2):
        q = Queue.Queue()
        r = []
        # read file
        fd = open(self.file,'r')
        for line in fd:
            arr = line.split(":")
            if len(arr) == 2:
                q.put(arr)
        tlist = []
        for i in xrange(self.tnum):
            cur = CheckThread(i,q,r)
            cur.start()
            tlist.append(cur)
        for cur in tlist:
            cur.join()
        print "All is OK!"
        print len(r)

def main():
    file1 = 'list.txt'
    file2 = 'check.txt'
    r = ProxyCheck(100,file1)
    r.run(file2)

main()

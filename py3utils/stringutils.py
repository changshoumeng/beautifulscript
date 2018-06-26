#!/usr/bin/python
# -*- coding: UTF-8 -*-
# python3+

import hashlib
import os


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of bytes

def file2str(fn):
    data=b''
    with open(fn,'rb') as rf:
        tmpdata=rf.read(4096)
        while tmpdata:
            data += tmpdata
            tmpdata = rf.read(4096)
    return to_str( data )

def str2file(fn,s):
    with open(fn,'wb') as wf:
        wf.write( to_bytes( s))


def str2md5(src=""):
    myMd5 = hashlib.md5()
    src = to_bytes(src)
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest


def cachehtml(workdir, url, data=""):
    if not data:
        return
    if not os.path.exists(workdir):
        os.mkdir(workdir)
    fn = str2md5(url)
    fn = os.path.join(workdir, fn)
    fn = fn + ".html"
    with open(fn, 'wb') as wf:
        data = to_bytes(data)
        wf.write(data)


def getcachehtml(workdir, url):
    if not os.path.exists(workdir):
        return ""
    fn = str2md5(url)
    fn = os.path.join(workdir, fn)
    fn = fn + ".html"
    if not os.path.exists(fn):
        return ""

    with open(fn, 'rb') as rf:
        return to_str(rf.read(1024 * 1024 * 16))


def outputcsv(workdir, uid, rlist=[]):
    if not rlist:
        return
    if not os.path.exists(workdir):
        os.mkdir(workdir)
    fn = str(uid)
    fn = os.path.join(workdir, fn)
    fn = fn + ".txt"
    with open(fn, 'wb') as wf:
        for r in rlist:
            r = list(r)
            r = map(lambda x: str(x), r)
            s = "\t".join(r)
            s += "\n"
            wf.write(to_bytes(s))
    print(fn)


def readheader():
    fn = 'header.txt'
    header = {}
    with open(fn, 'rb') as rf:
        for line in rf:
            line = to_str(line.strip())
            p = line.find(':')
            key = line[:p]
            val = line[p + 1:]
            print(key, val)
            header[key.strip()] = val.strip()
    return header


def httpsgetpage(url, res):
    import http.client as  httplib
    httpClient = None
    fullurl = "https://" + url + res
    try:
        httpClient = httplib.HTTPSConnection(url, timeout=6)
        httpClient.request("GET", res)
        response = httpClient.getresponse()
        print("httpsgetpage:{0},status:{1} reason:{2}".format(fullurl, response.status, response.reason))
        data = response.read()
        return data
    except Exception as  e:
        print("httpsgetpage:{0},caugth e:{1}".format(fullurl, str(e)))
        return
    finally:
        if httpClient:
            httpClient.close()


def httpgetpage(url, res):
    import http.client as  httplib
    httpClient = None
    fullurl = "http://" + url + res
    try:
        httpClient = httplib.HTTPConnection(url, timeout=6)
        httpClient.request("GET", res)
        response = httpClient.getresponse()
        print("httpgetpage:{0},status:{1} reason:{2}".format(fullurl, response.status, response.reason))
        data = response.read()
        return data
    except Exception as  e:
        print("httpgetpage:{0},caugth e:{1}".format(fullurl, str(e)))
        return
    finally:
        if httpClient:
            httpClient.close()


def httppostreq(url,res,param):
    import http.client as  httplib
    from  urllib import  parse
    httpClient = None
    fullurl = "http://" + url + res
    try:
        params = parse.urlencode( param)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        httpClient = httplib.HTTPConnection(url, timeout=6)
        httpClient.request("POST", res,params,headers)
        response = httpClient.getresponse()
        print("httppostreq:{0},status:{1} reason:{2}".format(fullurl, response.status, response.reason))
        data = response.read()
        return data
    except Exception as  e:
        print("httppostreq:{0},caugth e:{1}".format(fullurl, str(e)))
        return
    finally:
        if httpClient:
            httpClient.close()


# if __name__ == '__main__':
#     main()

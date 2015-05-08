#!/usr/bin/python
## -*- encoding: utf-8 -*-

from importHandler import declarative, logger
import logging, argparse, sys, json, httplib, urllib, requests


def make_request(url):
    url = 'http://tv.sohu.com/20150508/n412634245.shtml'
    params = {
        "url":urllib.quote_plus(url),
        "tgwCategory":58
    }
    headers = {
        "Cookie":"vjuids=-14c0020c5.14c2091aff6.0.16584e8f; fuid=14258639652813787643; vjlast=1426475561.1427676808.13; sci12=w:1; sohutag=8HsmeSc5NCwmcyc5NCwmYjc5NCwmYSc5NCwmZjc5NCwmZyc5NCwmbjc5NCwmaSc5NSwmdyc5NCwmaCc5NCwmYyc5NCwmZSc5NCwmbSc5NCwmdCc5NH0; FYID=2E1BFBCE0EC1B67932076C86BC39FD37; SUV=1503031649386771; JSESSIONID=aaafRPvn-xRSJbJAZ5j0u; UNION_KEY=Yvbyml2HcWS3IzBOGXVGb_PBRE9kCCNuqnYh4StQQNPnDwzdbDqyXg=="
    }
    r = requests.get("http://lm.tv.sohu.com/promotion/singlelink_code.do", params=params, headers=headers)
    if not r.status_code == '200':
        pass

    print r.status_code
    print r.json()

read from db
for each in result:
    id = each['id']
    url = each['url']
    if !already_converted(url):
        try:
            newUrl = make_get(url)
            update(each, newUrl)
        except Exception, e:
            print e
            raise e
        



# conn = httplib.HTTPSConnection("lm.tv.sohu.com")
# headers = {
#     "Cookie":"vjuids=-14c0020c5.14c2091aff6.0.16584e8f; fuid=14258639652813787643; vjlast=1426475561.1427676808.13; sci12=w:1; sohutag=8HsmeSc5NCwmcyc5NCwmYjc5NCwmYSc5NCwmZjc5NCwmZyc5NCwmbjc5NCwmaSc5NSwmdyc5NCwmaCc5NCwmYyc5NCwmZSc5NCwmbSc5NCwmdCc5NH0; FYID=2E1BFBCE0EC1B67932076C86BC39FD37; SUV=1503031649386771; JSESSIONID=aaafRPvn-xRSJbJAZ5j0u; UNION_KEY=Yvbyml2HcWS3IzBOGXVGb_PBRE9kCCNuqnYh4StQQNPnDwzdbDqyXg=="
# }
# url = 'http://tv.sohu.com/20150508/n412634245.shtml'
# print urllib.quote_plus(url)
# params = {
#     "url":urllib.quote_plus(url),
#     "tgwCategory":58
# }
# params = urllib.urlencode(params)
# print params
# conn.request("GET","/promotion/singlelink_code.do?",params,headers)
# res = conn.getresponse()
# print res.status, res.reason
# data = res.read()
# print data
# conn.close()

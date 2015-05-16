#!/usr/bin/python

from aws_signed_request import aws_signed_request
import urllib
from xml.dom import minidom

public_key = 'AKIAISA4M3LOL52SUIDQ'
private_key = 'WAlWog8VK33T7DSTxaCBUXtqIRCacxx4RTptkBSi'
associate_tag = 'th0426-20'

# generate signed URL
request = aws_signed_request('ecs.amazonaws.com/onca/xml', {
        'Operation': 'ItemSearch',
        'Service': 'AWSECommerceService',
        'SearchIndex': 'All',
        'Keywords': 'Computer',
        'AssociateTag': 'th0426-20',
        'ResponseGroup': 'Small'}, public_key, private_key, associate_tag)

# do request
try:
    response_obj = urllib.urlopen(request);
except IOError:
    print "Request failed."
else:
    response = response_obj.read()
    pxml = minidom.parseString(response)
    items = pxml.getElementsByTagName('Title')
    print items
    #print items[0].firstChild.nodeValue
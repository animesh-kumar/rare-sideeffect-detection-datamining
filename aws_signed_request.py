#!/usr/bin/python

import time
import urllib
import base64
import hmac
import hashlib

def aws_signed_request(region, params, public_key, private_key, associate_tag=None, version='2011-08-01'):
       
    # some paramters
    method = 'GET'
    host = 'webservices.amazon.' + region
    uri = '/onca/xml'
    
    # additional parameters
    params['Service'] = 'AWSECommerceService'
    params['AWSAccessKeyId'] = public_key
    params['Timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    params['Version'] = version
    if associate_tag:
        params['AssociateTag'] = associate_tag
    
    # create the canonicalized query
    canonicalized_query = [urllib.quote(param).replace('%7E', '~') + '=' + urllib.quote(params[param]).replace('%7E', '~')
                            for param in sorted(params.keys())]
    canonicalized_query = '&'.join(canonicalized_query)
    
    # create the string to sign
    string_to_sign = method + '\n' + host + '\n' + uri + '\n' + canonicalized_query;
    
    # calculate HMAC with SHA256 and base64-encoding
    signature = base64.b64encode(hmac.new(key=private_key, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    
    # encode the signature for the request
    signature = urllib.quote(signature).replace('%7E', '~')

    return 'http://' + host + uri + '?' + canonicalized_query + '&Signature=' + signature


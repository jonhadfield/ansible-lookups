# (c) 2016, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup returns your public IP by querying multiple services.

Example Usage:
{{ lookup('my_public_ip')) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase
import socket
from json import load
from urllib2 import urlopen

def is_valid_ip(value):
    try:
        socket.inet_aton(value)
        return True
    except socket.error:
        return False

class LookupModule(LookupBase):
    def run(self, terms, **kwargs):
        try:
            value = load(urlopen('http://httpbin.org/ip'))['origin']
            if is_valid_ip(value):
                return [value]
        except:
            pass
        try:
            value = load(urlopen('https://api.ipify.org/?format=json'))['ip']
            if is_valid_ip(value):
                return [value]
        except:
            pass
        try:
            value = load(urlopen('http://jsonip.com'))['ip']
            if is_valid_ip(value):
                return [value]
        except:
            pass


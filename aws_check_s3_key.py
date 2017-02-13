# (c) 2016, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a path and checks for the presence of a specific key in S3.
This may be used for failing early if an object isn't present or as part of a conditional upload task.

Example Usage:
{{ lookup('aws_ec2_instance_id_from_name', ('eu-west-1', 'mybucket/hello.txt') }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto3
except ImportError:
    raise AnsibleError("aws_check_s3_key lookup cannot be run without boto installed")
try:
    import simplejson as json
except ImportError:
    import json

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        split_path = terms[0][1].split('/')
        bucket = split_path[0]
        key = '/'.join(split_path[1:])
        s3 = boto3.client('s3')
        try:
            s3.head_object(Bucket=bucket, Key=key)
            return 'True'
        except:
            pass

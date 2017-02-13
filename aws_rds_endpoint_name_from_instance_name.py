# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and an RDS instance
name and returns the endpoint name.

Example Usage:
{{ lookup('aws_rds_endpoint_name_from_instance_name', ('eu-west-1', 'mydb')) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto.rds
except ImportError:
    raise AnsibleError("aws_rds_endpoint_name_from_instance_name lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        print(terms)
        region = terms[0][0]
        instance_name = terms[0][1]
        db_conn = boto.rds.connect_to_region(region)
        db = db_conn.get_all_dbinstances(instance_name)
        if db and db[0]:
            return [db[0].endpoint[0]]

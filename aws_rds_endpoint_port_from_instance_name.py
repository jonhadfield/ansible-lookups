# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and an RDS instance
name and returns the endpoint port.

Example Usage:
{{ lookup('aws_rds_endpoint_port_from_instance_name', ('eu-west-1', 'mydb')) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto3
    import botocore
except ImportError:
    raise AnsibleError("aws_rds_endpoint_port_from_instance_name lookup cannot be run without boto installed")


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        instance_name = terms[0][1]

        session=boto3.session.Session(region_name=region)

        try:
            rds_client=session.client('rds')
        except botocore.exceptions.NoRegionError:
            raise AnsibleError("AWS region not specified.")

        result=rds_client.describe_db_instances(DBInstanceIdentifier=instance_name)

        if result and result.get('DBInstances'):
            return [result.get('DBInstances')[0].get('Endpoint').get('Port').encode('utf-8')]
        return None

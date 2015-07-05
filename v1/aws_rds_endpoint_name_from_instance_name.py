# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and an RDS instance
name and returns the endpoint name.

Example Usage:
{{ lookup('aws_rds_endpoint_name_from_instance_name', ('eu-west-1', 'mydb')) }}
"""
from ansible import errors
try:
    import boto.rds
except ImportError:
    raise AnsibleError("aws_rds_endpoint_name_from_instance_name lookup cannot be run without boto installed")


class LookupModule(object):
    def __init__(self, basedir=None, **kwargs):
                                self.basedir = basedir

    def run(self, terms, variables=None, **kwargs):
        region = terms[0]
        instance_name = terms[1]
        db_conn = boto.rds.connect_to_region(region)
        db = db_conn.get_all_dbinstances(instance_name)
        if db and db[0]:
            return [db[0].endpoint[0]]
        return None

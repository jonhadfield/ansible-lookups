# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup retrieves the numerical id of the AWS account that
matches the discovered credentials. You might want to use this to check that 
Ansible is going to manage the correct account before you run any tasks.

Example Usage:
{{ lookup('aws_account_id') }}
"""
from ansible import errors
try:
    import boto
except ImportError:
    raise AnsibleError("aws_account_id lookup cannot be run without boto installed")


class LookupModule(object):
    def __init__(self, basedir=None, **kwargs):
                                self.basedir = basedir

    def run(self, **kwargs):
        iam_conn = boto.connect_iam() 
        if iam_conn:
            return [iam_conn.get_user().arn.split(':')[4]]

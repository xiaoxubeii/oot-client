__author__ = 'tardis'
from ootclient import server
import requests
import json
from ootclient.utils import patch_subprocess
import random


def _get_server_url():
    return _get_kernel_params('url')


def _get_kernel_params(key):
    subprocess = patch_subprocess()
    output = subprocess.check_output(['bash', '-c', 'cat /proc/cmdline'])
    params = output.split(' ')
    for p in params:
        kv = p.split('=')
        if key == kv[0]:
            return kv[1]
            # m = re.search(
            # r'(?<=' + key + '=)http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output)
            # if m:
            # return m.group().replace(' ', '')


def _get_master_cidr():
    return _get_kernel_params('master_cidr')


def notify_master_pxeboot():
    s = server.Server()
    headers = {'content-type': 'application/json'}
    msg = {
        # TODO
        'source_id': 'not_yet_impl_%s' % random.randint(1, 100),
        'msg': {
            'pxe_boot': 'success',
            'opt': {
                'server.init': (s(master_cidr=_get_master_cidr()),)
            }
        }
    }
    requests.post(_get_server_url() + '/notifies', data=json.dumps(msg), headers=headers)


notify_master_pxeboot()


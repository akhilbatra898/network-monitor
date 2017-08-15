
import json
import pytest
import platform

import psutil
import uptime

from .. import client_main


@pytest.fixture(scope='module')
def client_data():
    data = {"uptime": 31562.02,
            "cpu_usage": 0.0,
            "os": "Linux-4.8.0-52-generic-x86_64-with-Ubuntu-16.04-xenial",
            "memory_usage": 88.7,
            "machine_type": "x86_64"}
    return data


def test_client(mocker, client_data):
    mocker.patch('platform.platform')
    mocker.patch('platform.machine')
    mocker.patch('psutil.cpu_percent')
    mocker.patch('psutil.virtual_memory')
    mocker.patch('uptime.uptime')
    mocker.patch('json.dumps')
    platform.machine.return_value = client_data['machine_type']
    platform.platform.return_value = client_data['os']
    psutil.cpu_percent.return_value = client_data['cpu_usage']
    psutil.virtual_memory.return_value = ['', '', client_data['memory_usage']]
    uptime.uptime.return_value = client_data['uptime']
    client_main.get_client_data()
    json.dumps.assert_called_with(client_data)

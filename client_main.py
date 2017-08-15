
import platform
import json

import psutil
import uptime


def get_client_data():
    data = {}
    data['machine_type'] = platform.machine()
    data['os'] = platform.platform()
    data['cpu_usage'] = psutil.cpu_percent()
    data['memory_usage'] = psutil.virtual_memory()[2]
    data['uptime'] = uptime.uptime()
    data = json.dumps(data)
    print data


if __name__ == "__main__":
    get_client_data()

# Synology SRM API

[![Build status](https://github.com/aerialls/synology-srm/workflows/Test/badge.svg)](https://github.com/aerialls/synology-srm/actions?query=workflow%3ATest)
[![PyPi version](https://img.shields.io/pypi/v/synology-srm.svg)](https://pypi.org/project/synology-srm/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/synology-srm.svg)](https://pypi.python.org/pypi/synology-srm/)

Python 3 library to use the Synology SRM (Synology Router Manager) API. This is **NOT** the same thing as Synology DSM (DiskStation Manager).

This library should work with the following devices.

* RT1900ac
* RT2600ac

> It's not possible to create another account in SRM with admin permissions. You'll need to use your `admin` account (or the one you renamed at creation).

## Usage

```python
import synology_srm

client = synology_srm.Client(
    host='192.168.1.254',
    port=8001,
    https=True,
    username='admin',
    password='admin',
)
```

You can now access all namespaces from the API. The following methods are availabe.

* Base
  * getinfo_encryption()
  * query_info()
* Core
  * list_ddns_extip()
  * list_ddns_record()
  * get_system_utilization()
  * get_network_nsm_device(filters=`{}`)
  * get_ngfw_traffic(interval=`live|day|week|month`)
  * list_certificate()
  * export_certificate(path=`certificate.zip`)
* Mesh
  * get_network_wanstatus()
  * get_network_wifidevice()
  * get_system_info()

For instance, to list all endpoints available in the API.

```python
endpoints = client.base.query_info()

for endpoint, config in endpoints.items():
    print("API endpoint {} (minVersion={}, maxVersion={})".format(
        endpoint,
        config['minVersion'],
        config['maxVersion'],
    ))
```

## HTTPS auto-signed certificate

You can disable the HTTPS certificate verification if you are using a self-signed certificate.

```python
client.http.disable_https_verify()
```

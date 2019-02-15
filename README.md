# Synology SRM API

[![Build Status](https://travis-ci.org/aerialls/synology-srm.svg?branch=master)](https://travis-ci.org/aerialls/synology-srm)
[![PyPi Version](https://img.shields.io/pypi/v/synology-srm.svg)](https://pypi.org/project/synology-srm/)

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
  * encryption
  * info
* Core
  * system_utilization
* Mesh
  * network_wanstatus
  * network_wifidevice

For instance, to list all endpoints available in the API.

```python
endpoints = client.base.info()

for endpoint in endpoints:
    print(endpoint)
```

## HTTPS auto-signed certificate

You can disable the HTTPS certificate verification if you are using a self-signed certificate.

```python
client.http.disable_https_verify()
```

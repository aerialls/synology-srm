# Synology SRM API

[![Build Status](https://travis-ci.org/aerialls/synology-srm.svg?branch=master)](https://travis-ci.org/aerialls/synology-srm)
[![PyPi Version](https://img.shields.io/pypi/v/synology-srm.svg)](https://pypi.org/project/synology-srm/)

Python 3 library to use the Synology SRM (Synology Router Manager) API. This is **NOT** the same thing as Synology DSM (DiskStation Manager).

This library should work with the following devices.

* RT1900ac
* RT2600ac

## Usage

```python
import synology_srm

client = synology_srm.Client(
    host='192.168.1.254',
    port=8001,
    https=True
    username='admin',
    password='FZan7xw7eh3z9Zzj',
)
```

You can now access all different namespaces from the API. The only namespace available currently is `mesh` with the following method.

```python
devices = client.mesh.network_wifidevice()

for device in devices:
    print("Found device {} with MAC address {}".format(
        device['hostname'],
        device['mac']
    ))
```

## HTTPS auto-signed certificate

You can disable the HTTPS certificate verification if you are using a self-signed certificate.

```python
client.http.disable_https_verify()
```

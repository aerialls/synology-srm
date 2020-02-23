# Synology SRM API

[![Build status](https://github.com/aerialls/synology-srm/workflows/Test/badge.svg)](https://github.com/aerialls/synology-srm/actions?query=workflow%3ATest)
[![PyPi version](https://img.shields.io/pypi/v/synology-srm.svg)](https://pypi.org/project/synology-srm/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/synology-srm.svg)](https://pypi.python.org/pypi/synology-srm/)

<style>.bmc-button img{height: 34px !important;width: 35px !important;margin-bottom: 1px !important;box-shadow: none !important;border: none !important;vertical-align: middle !important;}.bmc-button{padding: 7px 10px 7px 10px !important;line-height: 35px !important;height:51px !important;min-width:217px !important;text-decoration: none !important;display:inline-flex !important;color:#ffffff !important;background-color:#FF813F !important;border-radius: 5px !important;border: 1px solid transparent !important;padding: 7px 10px 7px 10px !important;font-size: 28px !important;letter-spacing:0.6px !important;box-shadow: 0px 1px 2px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;margin: 0 auto !important;font-family:'Cookie', cursive !important;-webkit-box-sizing: border-box !important;box-sizing: border-box !important;-o-transition: 0.3s all linear !important;-webkit-transition: 0.3s all linear !important;-moz-transition: 0.3s all linear !important;-ms-transition: 0.3s all linear !important;transition: 0.3s all linear !important;}.bmc-button:hover, .bmc-button:active, .bmc-button:focus {-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;text-decoration: none !important;box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;opacity: 0.85 !important;color:#ffffff !important;}</style><link href="https://fonts.googleapis.com/css?family=Cookie" rel="stylesheet"><a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/aerialls"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a coffee"><span style="margin-left:15px;font-size:28px !important;">Buy me a coffee</span></a>

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
  * encryption()
  * info()
* Core
  * ddns_extip()
  * ddns_record()
  * system_utilization()
  * network_nsm_device(filters=`{}`)
  * ngfw_traffic(interval=`live|day|week|month`)
* Mesh
  * network_wanstatus()
  * network_wifidevice()
  * system_info()

For instance, to list all endpoints available in the API.

```python
endpoints = client.base.info()

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

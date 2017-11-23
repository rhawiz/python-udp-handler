# Python Logstash UDP Handler

UdpHandler for python logging module which overrides default DatagramHandler module.

DatagramHandler sends pickles logs and then sends over UDP socket which logstash can't read.

For this reason, we need to override its makePickle method to send logs in json format.

When we send logs in json format we don't need to do any formatting at logstash side.

### Installation & Usage

The module can be installed using pip

`pip install git+https://github.com/rhawiz/python-udp-handler.git`

Logging config file (config.conf)
```
# config.conf

[loggers]
keys=root

[handlers]
keys=udpHandler

[formatters]
keys=

[logger_root]
level=DEBUG
handlers=udpHandler

[handler_udpHandler]
class=logmodule.UdpHandler
level=DEBUG
args=('elk.internal.com', 33333)
```

[OPTIONAL] The path to the config file can be defined as an environment variable.

```
export LOGSTASH_CONFIG=/path/to/config/file
```

the logger can retrieved and used by calling the `get_logger()` method.

```python
# logging_test.py

from logmodule import get_logger

def main():
    logger = get_logger()
    logger.info("LOG MESSAGE")

if __name__ == "__main__":
    main()

```


If LOGSTASH_CONFIG env variable is not set, then the path to the configuration file must be passed inside the method

```python
logger = get_logger("/path/to/config/file")
```

The script above will produce the following message to logstash
```json
{
    "_index": "udp-2017.11.23",
    "_type": "test",
    "_id": "AV_pBIk4obcniRRjqduh",
    "_version": 1,
    "_score": 1,
    "_source": {
        "msg": "LOG MESSAGE",
        "process": 4016,
        "exc_info": null,
        "created": 1511442909.4687173,
        "module": "logging_test",
        "relativeCreated": 18.426179885864258,
        "thread": 139647647831808,
        "type": "test",
        "levelno": 20,
        "threadName": "MainThread",
        "pathname": "/home/USER/logging_test.py",
        "args": null,
        "funcName": "main",
        "filename": "logging_test.py",
        "lineno": 10,
        "@timestamp": "2017-11-23T13:15:09.487Z",
        "processName": "MainProcess",
        "stack_info": null,
        "name": "root",
        "@version": "1",
        "host": "192.168.XX.XX",
        "msecs": 468.7173366546631,
        "levelname": "INFO",
        "exc_text": null
    }
}
```

# Python Logstash UDP Handler

UdpHandler for python logging module which overrides default DatagramHandler module.

DatagramHandler sends pickles logs and then sends over UDP socket which logstash can't read.

For this reason, we need to override its makePickle method to send logs in json format.

When we send logs in json format we don't need to do any formatting at logstash side.

### Installation & Usage

The module can be installed using pip:

```bash
pip install https://github.com/rhawiz/python-udp-handler.git
```


A configuration file is required

### Test

Run tests

```bash
$ python setup.py test
```


### Contact

[Rawand Hawiz](r.hawiz@geophy.com)
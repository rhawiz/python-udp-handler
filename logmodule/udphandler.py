import json
import os
import socket
from logging.handlers import SocketHandler
import logging
import logging.handlers
import logging.config


class UdpHandler(logging.handlers.DatagramHandler):  # Inherit from logging.Handler
    """
    A handler class which writes logging records, in pickle format, to
    a datagram socket.  The pickle which is sent is that of the LogRecord's
    attribute dictionary (__dict__), so that the receiver does not need to
    have the logging module installed in order to process the logging event.

    To unpickle the record at the receiving end into a LogRecord, use the
    makeLogRecord function.

    """

    def __init__(self, host, port):
        """
        Initializes the handler with a specific host address and port.
        """
        SocketHandler.__init__(self, host, port)
        self.closeOnError = False

    def makeSocket(self):
        """
        The factory method of SocketHandler is here overridden to create
        a UDP socket (SOCK_DGRAM).
        """
        if self.port is None:
            family = socket.AF_UNIX
        else:
            family = socket.AF_INET
        s = socket.socket(family, socket.SOCK_DGRAM)
        return s

    def send(self, s):
        """
        Send a pickled string to a socket.

        This function no longer allows for partial sends which can happen
        when the network is busy - UDP does not guarantee delivery and
        can deliver packets out of sequence.
        """
        if self.sock is None:
            self.createSocket()
        self.sock.sendto(bytearray(s, 'utf-8'), self.address)

    def makePickle(self, record):
        """
        Pickles the record in binary format with a length prefix, and
        returns it ready for transmission across the socket.
        """
        ei = record.exc_info
        if ei:
            # just to get traceback text into record.exc_text ...
            dummy = self.format(record)
        # See issue #14436: If msg or args are objects, they may not be
        # available on the receiving end. So we convert the msg % args
        # to a string, save it as msg and zap the args.
        d = dict(record.__dict__)
        d['msg'] = record.getMessage()
        d['args'] = None
        d['exc_info'] = None
        # Issue #25685: delete 'message' if present: redundant with 'msg'
        d.pop('message', None)
        s = json.dumps(d)
        return s


class UdpHandlerError(ValueError):
    pass


def get_logger(config_file=None):
    """
    Creates UDP handler logger. If config file is not passed in, will check for the path in environment variables.
    If neither are passed, will raise UdpHandlerError.

    :param config_file: Path to config file, defaults to None.
    :return: logger
    :rtype: logging.Logger
    :raises UdpHandlerError
    """

    if config_file is None:
        config_file = os.environ.get("LOGSTASH_CONFIG", None)

    if config_file is None:
        raise UdpHandlerError(
            "No config file found. "
            "Either pass the file into this method, or set environment variable LOGSTASH_CONFIG=/path/to/config")

    if os.path.isfile(config_file) is False:
        raise UdpHandlerError("'{}' config file does not exist.".format(config_file))

    logging.config.fileConfig(config_file)

    logger = logging.getLogger()

    return logger

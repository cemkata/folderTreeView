import os
import sys
from abc import abstractmethod

class Tee(object):
    """
    duplicates streams to a file.
    credits : http://stackoverflow.com/q/616645
    """

    def __init__(self, filename, mode="a"):
        self.filename = filename
        self.mode = mode
        self.stream = None
        self.fp = None

    @abstractmethod
    def set_stream(self, stream):
        #assigns "stream" to some global variable e.g. sys.stdout
        pass

    @abstractmethod
    def get_stream(self):
        #returns the original stream e.g. sys.stdout
        pass

    def write(self, in_str):
        if in_str is not None:
            self.stream.write(in_str)
            self.fp.write(in_str)

    def flush(self):
        self.stream.flush()
        self.fp.flush()
        os.fsync(self.fp.fileno())

    def __enter__(self):
        self.stream = self.get_stream()
        self.fp = open(self.filename, self.mode)
        self.set_stream(self)

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if self.stream != None:
            self.set_stream(self.stream)
            self.stream = None

        if self.fp != None:
            self.fp.close()
            self.fp = None

    def isatty(self):
        return self.stream.isatty()

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.filename)

    __str__ = __repr__
    __unicode__ = __repr__

class StdoutTee(Tee):
    def set_stream(self, stream):
        sys.stdout = stream

    def get_stream(self):
        return sys.stdout

class StderrTee(Tee):
    def set_stream(self, stream):
        sys.stderr = stream

    def get_stream(self):
        return sys.stderr
import os
from time import time

import portalocker

PROJECT_ROOT = os.path.abspath(os.getcwd())
if "pfs" not in PROJECT_ROOT:
    print("\033[1;31mThis package must be run within the TJREVERB pFS directory!\033[0;0m")
    print("\033[1;33mAssuming this is being run as a test of the package, output to folder `pfs-output`\033[0;0m")
else:
    while not PROJECT_ROOT.endswith("pfs"):
        PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)


class SerialException(Exception):
    pass


class Serial:
    PROJECT_ROOT = os.path.join(PROJECT_ROOT, "pfs-output")

    def __init__(self, port=None, baudrate=9600, timeout=float('inf'), invert=False):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.invert = invert

        self.read_filename = None
        self.write_filename = None
        self.error = False

        if not os.path.exists(self.PROJECT_ROOT):
            os.makedirs(self.PROJECT_ROOT)

        if self.port:
            self.open()

    @property
    def is_open(self):
        return not (self.read_filename is None and self.write_filename is None)

    def open(self):
        if self.port is None:
            raise SerialException('Port must be configured before it can be used.')

        if self.error:
            raise SerialException(f'Serial port {self.port} has disconnected')

        r = 't' if self.invert else 'r'
        t = 'r' if self.invert else 't'

        self.read_filename = os.path.join(self.PROJECT_ROOT, self.port.replace('/', '+') + f'_pfs_{r}x.serial')
        self.write_filename = os.path.join(self.PROJECT_ROOT, self.port.replace('/', '+') + f'_pfs_{t}x.serial')

        if not os.path.exists(self.read_filename):
            with portalocker.Lock(self.read_filename, 'w') as rx:
                pass
        if not os.path.exists(self.write_filename):
            with portalocker.Lock(self.write_filename, 'w') as tx:
                pass

    def close(self):
        if self.error:
            raise SerialException(f'Serial port {self.port} has disconnected')

        if self.is_open:
            self.read_filename = None
            self.write_filename = None

    def flushInput(self):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if self.error:
            raise SerialException(f'Serial port {self.port} has disconnected')

        with portalocker.Lock(self.read_filename, 'w') as rx:
            pass

    def flushOutput(self):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if self.error:
            raise SerialException(f'Serial port {self.port} has disconnected')

        with portalocker.Lock(self.write_filename, 'w') as tx:
            pass

    def write(self, message):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if self.error:
            raise SerialException(f'Serial port {self.port} has disconnected')

        if type(message) != bytes:
            raise SerialException("Send the serial port bytes")

        with portalocker.Lock(self.write_filename, 'a') as tx:
            tx.write(message.decode('utf-8'))

    def read(self, size=1):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if self.error:
            raise SerialException(f'Serial port {self.port} has disconnected')

        if size > 1:
            print("\033[1;33mOnly one byte/call with reverb-serial\033[0;0m")

        start = time()
        while time() - start < self.timeout:
            rx_content = None
            with portalocker.Lock(self.read_filename, 'r', timeout=self.timeout) as rx:
                rx_content = rx.read()

            if rx_content:
                nb = rx_content[0].encode('utf-8')
                with portalocker.Lock(self.read_filename, 'w') as rx:
                    rx.write(rx_content[1:])
                return nb

        return b''

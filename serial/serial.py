import os
import json

I2C_SMBUS_BLOCK_MAX = 32

PROJECT_ROOT = os.path.abspath(os.getcwd())
#if "pfs" not in PROJECT_ROOT:
#    raise RuntimeError("This package must be run within the TJREVERB pFS directory!")
#while not PROJECT_ROOT.endswith("pfs"):
#    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)


class Serial:

	def __init__(self, port=None, baudrate=9600, timeout=None):
		if port == None:
			raise RuntimeError("Port not specified")
		self.port = port
		self.baudrate = baudrate
		self.timeout = timeout
		self.open(port)

	def open(self, port):
		self.path = os.path.join(PROJECT_ROOT, port)

	def write(self, message):
		try:
			with open(os.path.join(self.path, "write"), "r") as r:
				queue = json.load(r)
		except: queue = []

		with open(os.path.join(self.path, "write"), "w") as w:
			json.dump(queue+[message], w)

	def read(self, size=1):
		try:
			with open(os.path.join(self.path, "read"), "r") as r:
				queue = json.load(r)
		except: queue = []

		message = "\n".join(queue)

		with open(os.path.join(self.path, "read"), "w") as w:
                        json.dump(message[size:].split("\n"), w)

		return message[:size].encode("utf-8")


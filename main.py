import nfc
import binascii

NFC_READER_ID = "usb:054c:06c3" # Sony RC-S380は全てこのID. lsusbコマンドで確認可能.

class NFCReader:
	def on_connect(self, tag):
		self.idm = binascii.hexlify(tag._nfcid).decode()
		print(f"IDm detected: {self.idm}")
		return True

	def read(self):
		clf = nfc.ContactlessFrontend(NFC_READER_ID)
		try:
			clf.connect(rdwr={"on-connect": self.on_connect})
		finally:
			clf.close()

def get_serial():
	serial_number = "0000000000000000"
	with open("/proc/cpuinfo", "r") as f:
		for line in f:
			if line[0:6] == "Serial":
				serial_number = line[10:26]
	return serial_number

if __name__ == "__main__":
	serial_number = get_serial()
	print(f"{serial_number=}")
	client = NFCReader()
	while True:
		client.read()


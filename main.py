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

if __name__ == "__main__":
	client = NFCReader()
	while True:
		client.read()


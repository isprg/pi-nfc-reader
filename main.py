import binascii
import json

import nfc
import requests

NFC_READER_ID = "usb:054c:06c3" # Sony RC-S380は全てこのID. lsusbコマンドで確認可能.

class NFCReader:
	"""
	RFIDデバイスからRFIDを読み取る関数，取得したRFIDを保持する．

	Attributes
	----------
	idm : str
		RFIDデバイスから取得したRFID．
	"""
	def on_connect(self, tag):
		"""
		RFIDタグを検知した際に呼び出されるコールバック関数．
		"""
		self.idm = binascii.hexlify(tag._nfcid).decode()
		print(f"IDm detected: {self.idm}")

		try:
			update_device_status(self.idm)
		except requests.exceptions.ConnectionError as e:
			print(f"RFIDが正常に更新されませんでした．\n{e}")

		return True

	def read(self):
		"""
		RFIDデバイスとの接続を確立する．
		"""
		clf = nfc.ContactlessFrontend(NFC_READER_ID)
		try:
			clf.connect(rdwr={"on-connect": self.on_connect})
		finally:
			clf.close()

API_ENDPOINT = "http://localhost:1323/api/v1/devices"
default_headers = {"Content-Type": "application/json"}

def get_serial():
	"""
	Raspberry-Piの一意なシリアルナンバーを取得する．
	"""
	serial_number = "0000000000000000"
	with open("/proc/cpuinfo", "r") as f:
		for line in f:
			if line[0:6] == "Serial":
				serial_number = line[10:26]
	return serial_number

def post_device(serial_number):
	"""
	Rapberry-PiをREST API経由でDBにデバイスとして登録する．
	"""
	json_data = {"name": serial_number}
	r = requests.post(API_ENDPOINT, headers=default_headers, data=json.dumps(json_data))
	return r


def update_device_status(rfid, device_id=None):
	"""
	登録済みのデバイスのRFIDを更新する．
	"""
	if device_id:
		json_data = {"target": rfid}
		r = requests.put(f"{API_ENDPOINT}/{device_id}", headers=default_headers, data=json.dumps(json_data))
		return r

if __name__ == "__main__":
	serial_number = get_serial()
	print(f"{serial_number=}")
	try:
		post_device(serial_number)
	except requests.exceptions.ConnectionError as e:
		print(f"デバイスが正常に登録されませんでした．\n{e}")
	client = NFCReader()
	while True:
		client.read()

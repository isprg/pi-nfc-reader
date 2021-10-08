import nfc
import binascii

from logging import getLogger, Formatter, StreamHandler, DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = getLogger(__name__)
logger.setLevel(INFO)
format = Formatter("%(asctime)s - %(name)s - %(levelname)s:%(message)s")
# logger.setFormatter(format)
ch = StreamHandler()
ch.setLevel(INFO)
logger.addHandler(ch)

NFC_READER_ID = "usb::" # lsusb コマンドで確認可能

try:
    while True:
        clf = nfc.ContactlessFrontend(NFC_READER_ID)
        clf.connect(rdwr={"on-connect": on_nfc_connect})
        clf.close()
except Exception as e:
    logger.error("Pasoriを検出できませんでした")
    exit()

def on_nfc_connect(tag):
    idm = binascii.hexlify(tag.idm)
    logger.info(f"IDm detected: {idm}")
    return True

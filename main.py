import nfc
import binascii

from logging import getLogger, Formatter, StreamHandler, DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = getLogger(__name__)
format = Formatter("%(asctime)s - %(name)s - %(levelname)s:%(message)s")
ch = StreamHandler()
ch.setFormatter(format)
ch.setLevel(INFO)
logger.addHandler(ch)

NFC_READER_ID = "usb:054c:06c3" # Sony RC-S380は全てこのID. lsusbコマンドで確認可能.

try:
    def on_nfc_connect(tag):
        try:
            idm = binascii.hexlify(tag.idm).decode()
            logger.info(f"IDm detected: {idm}")
            return True
        except AttributeError: # tagにidm属性がない種類の場合のエラーハンドリング
            pass

    while True:
        clf = nfc.ContactlessFrontend(NFC_READER_ID)
        clf.connect(rdwr={"on-connect": on_nfc_connect})
        clf.close()

except Exception as e:
    logger.error(e)
    logger.error("Pasoriを検出できませんでした")
    exit()


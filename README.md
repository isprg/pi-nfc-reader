# 必要パッケージ

* nfcpy
`pip install nfcpy`でインストール
スクリプト内では`import nfc`で呼び出す

# このスクリプト実行時の注意点

Raspberry Pi OSの初期設定では、USBデバイスはroot権限でしか操作できないようになっているので、udevでUSBデバイスの権限を予め上書きしておく、もしくはスクリプトをsudoで実行する必要があります。

## pipenvを利用するには

pipenvを利用しているので`pipenv install`でスクリプトの依存関係をインストールし、`pipenv run py main.py`で実行できます。

## RFIDリーダーのIDがわからない

`lsusb`コマンドを実行することで、現在USBポートに接続されているデバイスのIDを確認することができます。
コード中では、`usb:XXXX:XXXX`の形で記述しておく必要があります。

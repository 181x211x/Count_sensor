卒論で作成した入退室カウントセンサーのプログラム


ローカルのみの入退室カウントセンサー
-- sensor.py

サーバーとクライアントで複数の場所を管理する
-- server.py
-- sensor_cl.py


**ローカルのみのセンサーはpython3.6とOpenCVがあればいける
**サーバとつなげる方は、ツイッターとwebsocketのインストールがいる

�@server.pyにポート番号とホストのipアドレスを入れて実行
�Asensor_cl.pyにポート番号とホストのipアドレス入れて実行する。

※macとラズパイならいけたけど、windowsだと通信時になぜか接続が切れる（未解決）



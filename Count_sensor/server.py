import cv2
from websocket_server import WebsocketServer
import os
from twython import Twython


client_count = 0
client0_sum = 0
client1_sum = 0

#新しいクライアントが接続して来た時の処理
def new_client(client, server):
    print("Hey all, a new client has joined us")
    global client_count
    client_count += 1
    print(client_count)

#クライアントの接続が切れた時の処理
def client_left(client, server):
	print("Hey all, a client has left from us")
	global client_count
	client_count -= 1
	print(client_count)

#クライアントからメッセージが来た時の処理
def send_msg_allclient(client, server,message):
    if client_count > 1:
        if int(message[1]) == 1:
            global client1_sum
            client1_sum = int(message[4])


        if int(message[1]) == 0:
            global client0_sum
            client0_sum = int(message[4])



        print("client0の残席数: " + str(client0_sum) + "  client1の残席数: " + str(client1_sum))
        if client0_sum <= 25 or client1_sum <= 25:
          CONSUMER_KEY = 'MkC9pkXRqK4lRQSJ5irgrx1o4'
          CONSUMER_SECRET = 'ICe5V6hTYQzBNSbodIL2JSGixsoyAVAlKcQLL89Fdw7Un64kml'
          ACCESS_KEY = '943079779980402689-ud2YbSLhAlOFM2gBZiblckEcwKV0a92'
          ACCESS_SECRET = 'kCO4HWo6o6FHRyXMLmln1fPl2Ser6P1Wnepvz7QobRawg'
          api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
          #時間を取得
          timestamp = 'date +%F_%H:%M:%S'
          current_time = os.popen(timestamp).readline().strip()

    if client1_sum == client0_sum:
        api.update_status(status= current_time+ 'client0の残席数: ' + str(client0_sum) + '  client1の残席数: ' + str(client1_sum) + 'どちらも混んでいます' )


    if client1_sum > client0_sum:
        api.update_status(status= current_time+ 'client0の残席数: ' + str(client0_sum) + '  client1の残席数: ' + str(client1_sum) + 'client1の方が空いています' )


    if client1_sum < client0_sum:
        api.update_status(status= current_time+ 'client0の残席数: ' + str(client0_sum) + '  client1の残席数: ' + str(client1_sum) + 'client0の方が空いています' )












    if client1_sum > client0_sum:
        print("client1の方が空いてるよ")

    elif client1_sum < client0_sum:
        print("client0の方が空いてるよ")

    elif client1_sum == client0_sum:
        print("どちらも同じくらいかな")








#メインルーティン
server = WebsocketServer(ポート番号, host='ホストのipアドレス')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(send_msg_allclient)
server.run_forever()

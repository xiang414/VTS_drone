import socket
import threading
import time

tello_address = ('192.168.8.102', 8889)
local_address = ('192.168.8.100', 8889)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_address)

def send(message):
  try:
    sock.sendto(message.encode(), tello_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))
  #time.sleep(delay)

def receive():
  while True:
    try:
      response, ip_address = sock.recvfrom(128)
      print("Received message: " + response.decode(encoding='utf-8'))
    except Exception as e:
      sock.close()
      print("Error receiving: " + str(e))
      break

receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

send("command")
time.sleep(1)
send("battery?")
time.sleep(1)
sock.close()

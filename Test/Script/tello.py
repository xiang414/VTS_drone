import socket
import threading
import time

tello_address = ('172.20.10.3', 8889)
local_address = ('172.20.10.2', 8889)

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
"""
box_leg_distance = 50
yaw_angle = 90

send("command")
send("takeoff")
time.sleep(3)
#send("back " + str(50) , 4)
#send("left " + str(20) , 4)
#send("ccw " + str(179))
#time.sleep(3)
send("rc 0 20 0 0")
time.sleep(4)
send("rc 0 10 0 0")
time.sleep(4)
send("rc 0 0 0 0")
time.sleep(2)
# Yaw right
#send("cw " + str(yaw_angle), 3)
"""
while(True):
    
send("land")
print("Mission completed successfully!")
sock.close()

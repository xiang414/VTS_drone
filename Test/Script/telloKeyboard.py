# -*- coding: utf-8 -*-
import socket
import threading
import time
import tkinter as tk
from tkinter import messagebox

#tello_address = ('172.20.10.3', 8889)
#local_address = ('172.20.10.2', 8889)
#tello_address = ('192.168.0.101', 8889)
#tello_address1 = ('192.168.0.102', 8889)

#local_address = ('192.168.0.117', 8889)
#tello_address = ('192.168.0.110', 8889)
local_address = ('192.168.8.101', 8889)
tello_address = ('192.168.8.102', 8889)
#local_address = ('192.168.0.111', 8889)
#tello_address = ('192.168.0.100', 8889)
#local_address = ('192.168.31.51', 8889)
#tello_address = ('192.168.31.50', 8889)
#tello_address = ('192.168.0.102', 8889)
#local_address = ('192.168.0.100', 8889)
#local_address = ('192.168.8.102', 8889)
#tello_address = ('192.168.8.101', 8889)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_address)

def send(message):
  try:
    sock.sendto(message.encode(), tello_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))
#"""
def receive():
  while True:
      try:
        response, ip_address = sock.recvfrom(128)
        print("Received message: " + response.decode(encoding='utf-8'))
        #messagebox.showinfo('訊息' , response.decode(encoding='utf-8'))
      except Exception as e:
        sock.close()
        print("Error receiving: " + str(e))
        break
#"""
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

# Tell the user what to do
print('Type in a Tello SDK command and press the enter key. Enter "quit" to exit this program.')

# Loop infinitely waiting for commands or until the user types quit or ctrl-c
while True:
  try:
    message = input('')
    send(message)
    if 'quit' in message:
      print("Program exited sucessfully")
      sock.close()
      break
    
  # Handle ctrl-c case to quit and close the socket
  except KeyboardInterrupt as e:
    sock.close()
    break

"""
def unlock():
    try:
        message = str("command")
        sock.sendto(message.encode(), tello_address)
        response, ip_address = sock.recvfrom(128)   
    except Exception as e:
        print("Error sending: " + str(e))
    messagebox.showinfo('飛機狀態' , response.decode(encoding='utf-8'))

def unlock1():
    try:
        message = str("command")
        sock.sendto(message.encode(), tello_address)
        response, ip_address = sock.recvfrom(128)   
    except Exception as e:
        print("Error sending: " + str(e))
    messagebox.showinfo('飛機狀態' , response.decode(encoding='utf-8'))
    
def battery():
    try:
        message = str("battery?")
        sock.sendto(message.encode(), tello_address)
        response, ip_address = sock.recvfrom(128)   
    except:
        messagebox.showinfo('通知' , '錯誤')
    messagebox.showinfo('電池電量' , response.decode(encoding='utf-8'))
    
def wifi():
    try:
        message = str("ap HUAWEI-9C3E 123456789") #HUAWEI-30F2 123456789
        sock.sendto(message.encode(), tello_address)
        response, ip_address = sock.recvfrom(128)   
    except:
        messagebox.showinfo('通知' , '錯誤')
    messagebox.showinfo('wifi' , response.decode(encoding='utf-8'))
def rc():
    try:
        message = str("rc 4 19 0 0")
        sock.sendto(message.encode(), tello_address)
        response, ip_address = sock.recvfrom(128)  
    except:
        messagebox.showinfo('通知' , '錯誤')
    
def rc0():
    try:
        message = str("rc 0 0 0 0")
        sock.sendto(message.encode(), tello_address)
        response, ip_address = sock.recvfrom(128)
    except:
        messagebox.showinfo('通知' , '錯誤')

def land():
    try:
        message = str("land")
        sock.sendto(message.encode(), tello_address)
        response, ip_address = sock.recvfrom(128)
    except:
        messagebox.showinfo('通知' , '錯誤')
def takeoff():
    try:
        message = str("takeoff")
        sock.sendto(message.encode(), tello_address)
        response, ip_address = sock.recvfrom(128)   
    except Exception as e:
        print("Error sending: " + str(e))
    messagebox.showinfo('takeoff' , response.decode(encoding='utf-8'))
    
windows = tk.Tk()
windows.geometry('640x480')
windows.title('Tello')
group = tk.Frame(windows , bg = 'blue' , width = 640 , height = 480)
group.pack()
btn = tk.Button(group , text = '電量' , command = battery , width = 15 , height = 6)
btn.place(rely = 0.25 , relx = 0.75 , anchor = 'center')
btn1 = tk.Button(group , text = '解鎖' , command = unlock , width = 15 , height = 6)
btn1.place(rely = 0.25 , relx = 0.25 , anchor = 'center')
btn2 = tk.Button(group , text = 'wifi' , command = wifi , width = 15 , height = 6)
btn2.place(rely = 0.5 , relx = 0.5 , anchor = 'center')
btn3 = tk.Button(group , text = '飛' , command = rc , width = 15 , height = 6)
btn3.place(rely = 0.75 , relx = 0.25 , anchor = 'center')
btn4 = tk.Button(group , text = '停' , command = rc0 , width = 15 , height = 6)
btn4.place(rely = 0.75 , relx = 0.75 , anchor = 'center')
btn5 = tk.Button(group , text = '降落' , command = land , width = 15 , height = 6)
btn5.place(rely = 0.75 , relx = 0.5 , anchor = 'center')
btn6 = tk.Button(group , text = '起飛' , command = takeoff , width = 15 , height = 6)
btn6.place(rely = 0.25 , relx = 0.5 , anchor = 'center')
#btn7 = tk.Button(group , text = '起飛' , command = unlock1 , width = 15 , height = 6)
#btn7.place(rely = 0.85 , relx = 0.5 , anchor = 'center')
windows.mainloop()
"""

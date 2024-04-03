import cv2
import imutils
import pickle
import socket
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("HOST IP:", host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5) #  5 here means that 5 connections are kept waiting if the server is busy and if a 6th socket trys to connect then the connection is refused.

print("LISTENING AT:", socket_address)
#  Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print("GOT CONNECTION FROM:", addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while(vid.isOpened()):
            img, frame = vid.read()
            frame = imutils.resize(frame, width= 320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)

            cv2.imshow("TRANSMITTING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                client_socket.close()
                break
cv2.destroyAllWindows()

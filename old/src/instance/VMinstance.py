from flask import Flask
import socket
app=Flask(__name__)
@app.route('/')
def VMinstance():
    hostname=socket.gethostname()
    ip_adress=socket.gethostbyname(hostname)
    return "My IP adress is "+str(ip_adress)
    

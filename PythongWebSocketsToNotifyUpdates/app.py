# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# Function to update data in the background
def update_data():
    while True:
        time.sleep(5)  # Simulating data update every 5 seconds
        data = {'value': time.strftime('%H:%M:%S')}
        socketio.emit('update', data)
        if int(time.strftime('%S')) % 10 == 0:  # Example condition for sending notification every 10 seconds
            notification = {'message': 'Notification: Current time ends with 0!'}
            socketio.emit('notification', notification)

# Route for serving the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket event handler for connecting clients
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Start the background thread for updating data
thread = threading.Thread(target=update_data)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    socketio.run(app,allow_unsafe_werkzeug=True)

#!/usr/bin/env python3
import webbrowser
import time
import threading

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    threading.Thread(target=open_browser, daemon=True).start()
    from web_app import app, socketio
    socketio.run(app, debug=False, host='0.0.0.0', port=5000, log_output=False)
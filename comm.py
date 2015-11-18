#this is the interface to communicate from the gui framework with the server

try:
    import cPickle as pickle
except:
    import pickle

import socket
import struct
import threading

buffer_size = 16;

#write object
def _write(_socket, obj):
    data = pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
    _socket.send(struct.pack("=i", len(data)))
    _socket.send(struct.pack("="+str(len(data))+"s", data))

#read object
def _read(_socket):
    length = struct.unpack("=i", _socket.recv(4))[0]
    return pickle.loads(struct.unpack("="+str(length)+"s", _socket.recv(length))[0])

#register real object
class _ServiceBackend(object):

    _delegate = None
    _t = None
    _s = None
    _running = True

    def __init__(self, delegate):
        self._s = socket.socket()
        self._s.bind(("127.0.0.1", 3138))
        self._s.listen(0)
        self._delegate = delegate
        self._t = threading.Thread(target=self._run_read)
        self._t.daemon = True
        self._t.start()

    def stop(self):
        self._running = False
        self._s.close()

    def _run_read(self):
        while self._running:
            try:
                conn, addr = self._s.accept()
                conn.settimeout(5)

                while self._running:
                    command = _read(conn)
                    if command == "get_instances":
                        _write(conn, self._delegate.get_instances())
                    elif command == "get_steamid":
                        instance = _read(conn)
                        _write(conn, self._delegate.get_steamid(instance))
                    elif command == "get_apps":
                        instance = _read(conn)
                        _write(conn, self._delegate.get_apps(instance))
                    elif command == "update_app":
                        instance = _read(conn)
                        app_id = _read(conn)
                        _write(conn, self._delegate.update_app(instance, app_id))
                    elif command == "start_game":
                        instance = _read(conn)
                        app_id = _read(conn)
                        _write(conn, self._delegate.start_game(instance, app_id))
                    elif command == "launch_client":
                        ip = _read(conn)
                        port = _read(conn)
                        auth = _read(conn)
                        app_id = _read(conn)
                        instance = _read(conn)
                        _write(conn, self._delegate.launch_client(ip, port, auth, app_id, instance))
                    elif command == "end":
                        conn.close()
                        break
            except:
                import traceback
                traceback.print_exc()


#call proxy object
class Service(object):

    _s = None

    def __enter__(self):
        self._s = socket.socket()
        self._s.connect(("127.0.0.1", 3138))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _write(self._s, "end")
        self._s.close()

    def get_instances(self):
        _write(self._s, "get_instances")
        return _read(self._s)

    def get_steamid(self, instance):
        _write(self._s, "get_steamid")
        _write(self._s, instance)
        return _read(self._s)

    def get_apps(self, instance):
        _write(self._s, "get_apps")
        _write(self._s, instance)
        return _read(self._s)

    def update_app(self, instance, app_id):
        _write(self._s, "update_app")
        _write(self._s, instance)
        _write(self._s, app_id)
        return _read(self._s)

    def start_game(self, instance, app_id):
        _write(self._s, "start_game")
        _write(self._s, instance)
        _write(self._s, app_id)
        return _read(self._s)

    def launch_client(self, ip, port, auth, app_id, instance):
        _write(self._s, "launch_client")
        _write(self._s, ip)
        _write(self._s, port)
        _write(self._s, auth)
        _write(self._s, app_id)
        _write(self._s, instance)
        return _read(self._s)

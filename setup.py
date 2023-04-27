import logging
import os
import sys

# See https://setuptools.pypa.io/en/latest/userguide/quickstart.html
from setuptools import setup

def launch_http_server(directory):
    assert os.path.isdir(directory)

    try:
        try:
            from SimpleHTTPServer import SimpleHTTPRequestHandler
        except ImportError:
            from http.server import SimpleHTTPRequestHandler

        try:
            import SocketServer
        except ImportError:
            import socketserver as SocketServer

        import socket

        for port in [80] + list(range(8000, 8100)):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('localhost', port))
                s.close()
            except socket.error as e:
                logging.debug("Can't use port %d: %s" % (port, e.strerror))
                continue

            print("HTML coverage report now available at http://{}{}".format(
                socket.gethostname(), (":%s" % port) if port != 80 else ""))

            os.chdir(directory)
            SocketServer.TCPServer(("", port),
                SimpleHTTPRequestHandler).serve_forever()
        else:
            logging.debug("All network port. ")
    except Exception as e:
        logging.error("ERROR: while starting an HTTP server to serve "
                      "the coverage report: %s" % e)


command = sys.argv[-1]
if command == 'publish':
    os.system('rm -rf dist')
    os.system('python3 setup.py bdist_wheel')
    os.system('twine upload dist/*whl dist/*gz')
    sys.exit()
elif command == "coverage":
    try:
        import coverage
    except ModuleNotFoundError:
        sys.exit("coverage.py not installed (pip install --user coverage)")
    setup_py_path = os.path.abspath(__file__)
    os.system('coverage run --source=configargparse ' + setup_py_path +' test')
    os.system('coverage report')
    os.system('coverage html')
    print("Done computing coverage")
    launch_http_server(directory="htmlcov")
    sys.exit()

# See setup.cfg
setup()

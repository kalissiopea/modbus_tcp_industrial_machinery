import argparse
import logging
from pyModbusTCP.server import ModbusServer

# init logging
logging.basicConfig()
# parse args
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', type=str, default='localhost', help='Host (default: localhost)')
parser.add_argument('-p', '--port', type=int, default=1502, help='TCP port (default: 1502)')
parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
args = parser.parse_args()
# logging setup
if args.debug:
    logging.getLogger('pyModbusTCP.server').setLevel(logging.DEBUG)

server = ModbusServer(host=args.host, port=args.port)

# start modbus server
print("Start Server...")
print("Server is online")
server.start()


#after keyboardInterrupt
print("Shutdown Server...")
print("Server is offline")

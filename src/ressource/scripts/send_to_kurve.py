import socket
import time
import argparse
from datetime import datetime

class Logger:
    def __init__(self, output_file=""):
        self.output_file = output_file

    def log(self, message):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = "{} : [SEND_TO_KURVE] {}".format(dt, message)
        if not self.output_file:
            print(log_line)
        else:
            with open(self.output_file, 'a') as f:
                f.write(log_line + '\n')

class KurveSender:
    def __init__(self, host, port, logger):
        self.host = host
        self.port = port
        self.logger = logger

    def send(self, message):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            self.logger.log("SENDING {}".format(message))
            sock.sendall(message + '\n')
            self.logger.log("READ RESPONSE")
            response = sock.recv(1024).strip()
            self.logger.log("PARSE RESPONSE")
            if response != "INSERT OK":
                self.logger.log("KPI Server returned unexpected error [{}].".format(response))
                return 2
            return 0
        except socket.error as e:
            self.logger.log("Cannot connect to KPI Server: {}".format(e))
            return 1
        finally:
            if sock:
                sock.close()

class RetrySender:
    def __init__(self, sender, max_attempts, sleep_time, logger):
        self.sender = sender
        self.max_attempts = max_attempts
        self.sleep_time = sleep_time
        self.logger = logger

    def send_with_retry(self, message):
        ret = 1
        attempt = 0
        while ret != 0:
            self.logger.log("SEND TO KURVE ATTEMPT #{}".format(attempt))
            ret = self.sender.send(message)
            self.logger.log("RET={}".format(ret))
            if attempt >= self.max_attempts:
                self.logger.log("MAX ATTEMPT REACHED : EXITING")
                exit(1)
            attempt += 1
            if ret != 0:
                time.sleep(self.sleep_time)

class KurveClient:
    def __init__(self, max_attempts, sleep_time, output_file, host, port):
        self.logger = Logger(output_file)
        self.sender = KurveSender(host, port, self.logger)
        self.retry_sender = RetrySender(self.sender, max_attempts, sleep_time, self.logger)

    def run(self, message):
        self.retry_sender.send_with_retry(message)

def main():
    parser = argparse.ArgumentParser(description='Send message to KPI server.')
    parser.add_argument('-m', '--max-attempt', type=int, default=10,
                        help='Maximum number of attempts (default: 10)')
    parser.add_argument('-s', '--sleep-time', type=int, default=10,
                        help='Sleep time between attempts in seconds (default: 10)')
    parser.add_argument('-o', '--output-file', default="",
                        help='Output file for logging (default: stdout)')
    parser.add_argument('--host', default="192.168.98.94",
                        help='KPI server host (default: 192.168.98.94)')
    parser.add_argument('--port', type=int, default=8443,
                        help='KPI server port (default: 8443)')
    parser.add_argument('message', nargs='+',
                        help='Message to send to the KPI server')

    args = parser.parse_args()

    client = KurveClient(args.max_attempt, args.sleep_time, args.output_file, args.host, args.port)
    message = ' '.join(args.message)
    client.run(message)

if __name__ == '__main__':
    main()
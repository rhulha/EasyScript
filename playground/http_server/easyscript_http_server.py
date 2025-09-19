import socket
import threading
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from easyscript.easyscript import EasyScriptEvaluator, TokenType

class HTTPEasyScriptEvaluator(EasyScriptEvaluator):
    def __init__(self, request_data=None):
        super().__init__()
        self.request_data = request_data or ""
        self.log_output = []
    
    def parse_function_call(self, function_name: str):
        """Override function call parsing to add read() and capture log() output"""
        self.consume_token()  # consume '('

        args = []
        while self.current_token().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.consume_token()

        self.consume_token()  # consume ')'

        if function_name == 'len':
            if len(args) != 1:
                raise TypeError(f"len() takes exactly one argument ({len(args)} given)")
            return len(args[0])
        elif function_name == 'log':
            if len(args) != 1:
                raise TypeError(f"log() takes exactly one argument ({len(args)} given)")
            value = str(args[0])
            self.log_output.append(value)
            return value
        elif function_name == 'read':
            if len(args) != 0:
                raise TypeError(f"read() takes no arguments ({len(args)} given)")
            return self.request_data
        else:
            raise NameError(f"Function '{function_name}' is not defined")
    
    def get_log_output(self):
        return '\n'.join(self.log_output)
    
    def clear_log_output(self):
        self.log_output = []


def handle_client(client_socket, address):
    """Handle a single HTTP client connection"""
    try:
        print(f"[INFO] Connection from {address}")
        
        print(f"[DEBUG] Waiting for request data from {address[0]}...")
        request_data = client_socket.recv(4096).decode('utf-8')
        print(f"[DEBUG] Received {len(request_data)} bytes")
        
        if not request_data:
            print(f"[DEBUG] No data received from {address[0]}")
            return
        
        print(f"[DEBUG] Request from {address[0]}:")
        print(f"  {request_data.split()[0]} {request_data.split()[1] if len(request_data.split()) > 1 else '/'}")
        
        evaluator = HTTPEasyScriptEvaluator(request_data)
        try:
            with open("http_server.es", 'r', encoding='utf-8') as f:
                easyscript_code = f.read()
            evaluator.evaluate(easyscript_code)
            response = evaluator.get_log_output()
            
        except Exception as e:
            print(f"[ERROR] EasyScript execution error: {e}")
            response = f"""HTTP/1.1 500 Internal Server Error\r
Content-Type: text/html\r
Connection: close\r
\r
<html>
<head><title>500 - EasyScript Error</title></head>
<body>
<h1>500 - EasyScript Execution Error</h1>
<p>Error: {e}</p>
</body>
</html>"""
        
        # Send the response with proper HTTP line endings
        # Convert LF to CRLF for proper HTTP format
        response = response.replace('\n', '\r\n')
        client_socket.send(response.encode('utf-8'))
        
    except Exception as e:
        print(f"[ERROR] Error handling client {address}: {e}")
        error_response = """HTTP/1.1 500 Internal Server Error\r
Content-Type: text/html\r
Connection: close\r
\r
<html><body><h1>500 - Server Error</h1></body></html>"""
        try:
            client_socket.send(error_response.encode('utf-8'))
        except:
            pass
    finally:
        client_socket.close()


def start_server(host='localhost', port=8080):
    """Start the HTTP server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"[INFO] EasyScript HTTP Server started on http://{host}:{port}")
        print(f"[INFO] Press Ctrl+C to stop the server")
        print(f"[INFO] The server will execute http_server.es for each request")
        print()
        
        while True:
            client_socket, address = server_socket.accept()
            # Handle each client in a separate thread
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down...")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Check if http_server.es exists
    script_path = Path(__file__).parent / "http_server.es"
    if not script_path.exists():
        print("[WARNING] http_server.es not found in current directory.")
        print("          The server will still start, but requests will return 404.")
        print()
    
    start_server()
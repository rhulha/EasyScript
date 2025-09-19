import socket
import threading
from datetime import datetime


def handle_client(client_socket, address):
    """Handle a single HTTP client connection"""
    try:
        print(f"[INFO] Connection from {address}")
        
        # Receive the HTTP request
        request_data = client_socket.recv(4096).decode('utf-8')
        
        if not request_data:
            print(f"[DEBUG] No data received from {address[0]}")
            return
        
        # Parse the request line
        lines = request_data.split('\r\n')
        if lines:
            request_line = lines[0]
            parts = request_line.split()
            if len(parts) >= 2:
                method = parts[0]
                path = parts[1]
                print(f"[DEBUG] {method} {path} from {address[0]}")
            else:
                method = "UNKNOWN"
                path = "/"
        
        # Generate a simple response
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        response_body = f"""<!DOCTYPE html>
<html>
<head>
    <title>Simple HTTP Server</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ color: #333; }}
        .info {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1 class="header">Simple HTTP Server</h1>
    <div class="info">
        <p><strong>Method:</strong> {method}</p>
        <p><strong>Path:</strong> {path}</p>
        <p><strong>Client IP:</strong> {address[0]}</p>
        <p><strong>Time:</strong> {current_time}</p>
    </div>
    <p>This is a basic HTTP server written in Python.</p>
</body>
</html>"""

        # Create HTTP response
        response = f"""HTTP/1.1 200 OK\r
Content-Type: text/html\r
Content-Length: {len(response_body)}\r
Connection: close\r
\r
{response_body}"""
        
        # Send the response
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
        
        print(f"[INFO] Simple HTTP Server started on http://{host}:{port}")
        print(f"[INFO] Press Ctrl+C to stop the server")
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
    start_server()
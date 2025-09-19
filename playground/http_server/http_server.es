# EasyScript HTTP Server
# This script demonstrates handling HTTP requests using EasyScript

log("HTTP/1.1 200 OK")
log("Content-Type: text/html")
log("Connection: close")
log("")  # Empty line to separate headers from body

# Parse the request to extract some basic information
log("<html>")
log("<head><title>EasyScript HTTP Server</title></head>")
log("<body>")
log("<h1>Welcome to EasyScript HTTP Server!</h1>")
log("<p>Your request was processed by EasyScript v0.5.0</p>")
log("<hr>")
log("<h2>Request Information:</h2>")
log("<pre>")
log(read())
log("</pre>")
log("<hr>")
log("<h2>Server Information:</h2>")
log("<p>Server Date: " + month + "/" + day + "/" + year + "</p>")
log("<p>EasyScript can handle HTTP requests!</p>")
log("<p>Request length: " + len(read()) + " characters</p>")

# Demonstrate conditional logic
if len(read()) > 100
    log("<p><strong>This is a large request!</strong></p>")

# Check if it's a GET request
if read() ~ "GET.*"
    log("<p> This is a GET request</p>")

# Check for specific paths
if read() ~ "GET /hello.*"
    log("<h3>Special Hello Page!</h3>")
    log("<p>You accessed the hello endpoint!</p>")

log("</body>")
log("</html>")
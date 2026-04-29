import http.server
import socketserver
import sys

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Custom success message for your project
        response = """
        <html>
        <head><title>Success</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1 style="color: #2ecc71;">MCA Project: Jenkins-K8s Pipeline Successful!</h1>
            <p style="font-size: 1.2em;">Status: <b>Pod is Running</b></p>
            <p>TGPCET Nagpur - Cloud Computing Assignment</p>
        </body>
        </html>
        """
        self.wfile.write(response.encode("utf-8"))

# 0.0.0.0 is crucial for Docker/Kubernetes networking
Handler = MyHandler

if __name__ == '__main__':
    print(f"Starting server at 0.0.0.0:{PORT}")

    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)


from flask import Flask, jsonify
from app.server_routes import create_session, send_message, end_session

app = Flask(__name__)

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Route definitions
app.add_url_rule('/create_session', view_func=create_session, methods=['POST'])
app.add_url_rule('/send_message', view_func=send_message, methods=['POST'])
app.add_url_rule('/end_session', view_func=end_session, methods=['POST'])
if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, jsonify
import argparse
import logging
from api_blueprints.user_bp import user_routes
from api_blueprints.health_bp import health_routes

logging.basicConfig(format='[%(levelname)s] %(name)s - %(asctime)s - %(message)s')
logger = logging.getLogger('PIC-API')
logger.setLevel(logging.INFO)

app = Flask(__name__)

app.register_blueprint(user_routes, url_prefix="/api/v1")
app.register_blueprint(health_routes, url_prefix="/health")

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "api not defined"}), 404

def parse_args():
    parser = argparse.ArgumentParser(description='Pic Web API')
    parser.add_argument("-d", "-debug", dest="debug", action='store_true', help='set true to enable debug mode')
    parser.add_argument("-p", "--port", dest="port", type=int, default=5000, help='exposed port')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    app.run(debug=args.debug, port=args.port)

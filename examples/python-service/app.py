"""
Production-ready Flask API with health checks and error handling
"""
from flask import Flask, jsonify, request
import os
import time
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

VERSION = os.getenv('VERSION', '1.0.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

@app.route('/health', methods=['GET'])
def health():
    """Health check for load balancers"""
    return jsonify({
        'status': 'healthy',
        'version': VERSION,
        'environment': ENVIRONMENT,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness check for Kubernetes"""
    checks = {
        'database': 'ok',
        'cache': 'ok'
    }
    
    all_healthy = all(status == 'ok' for status in checks.values())
    
    return jsonify({
        'status': 'ready' if all_healthy else 'not_ready',
        'checks': checks
    }), 200 if all_healthy else 503

@app.route('/api/v1/data', methods=['GET'])
def get_data():
    """Get data endpoint"""
    logger.info("GET /api/v1/data")
    
    return jsonify({
        'data': [
            {'id': 1, 'name': 'Item 1', 'value': 100},
            {'id': 2, 'name': 'Item 2', 'value': 200},
            {'id': 3, 'name': 'Item 3', 'value': 300}
        ],
        'count': 3,
        'version': VERSION
    }), 200

@app.route('/api/v1/data', methods=['POST'])
def create_data():
    """Create data endpoint"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    time.sleep(0.1)
    logger.info(f"POST /api/v1/data: {data}")
    
    return jsonify({
        'status': 'created',
        'data': data,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info(f"Starting app v{VERSION} in {ENVIRONMENT}")
    # Note: This is only for local development
    # Production uses Gunicorn (see Dockerfile)
    app.run(host='127.0.0.1', port=8080, debug=False)
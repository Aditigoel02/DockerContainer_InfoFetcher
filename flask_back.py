# backend/app.py

from flask import Flask, jsonify, request
import docker

app = Flask(__name__)

# Initialize Docker client
docker_client = docker.from_env()

@app.route('/containers', methods=['GET'])
def get_containers():
    try:
        # Fetch list of containers
        containers = docker_client.containers.list()
        container_info = [{'id': container.id, 'name': container.name, 'status': container.status} for container in containers]
        return jsonify(container_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/containers/<container_id>/<action>', methods=['POST'])
def perform_container_action(container_id, action):
    try:
        # Get container object
        container = docker_client.containers.get(container_id)
        # Perform action based on user input
        if action == 'start':
            container.start()
        elif action == 'stop':
            container.stop()
        elif action == 'restart':
            container.restart()
        else:
            return jsonify({'error': 'Invalid action'}), 400
        return jsonify({'message': f'Container {action}ed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

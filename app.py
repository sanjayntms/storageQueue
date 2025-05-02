from flask import Flask, request, render_template, redirect, url_for
from azure.storage.queue import QueueServiceClient
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import os
import json
from uuid import uuid4

app = Flask(__name__)

# Get Azure Storage Connection String from environment variable
STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
if not STORAGE_CONNECTION_STRING:
    print("Error: AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
    # You might want to exit the application here or provide a default for local testing
    # For example: STORAGE_CONNECTION_STRING = "your_default_connection_string_for_local"

QUEUE_NAME = "image-processing-queue"
UPLOADED_CONTAINER_NAME = "uploaded-images"
PROCESSED_CONTAINER_NAME = "processed-images"

# Initialize Queue Service Client
queue_service_client = QueueServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
queue_client = None
try:
    queue_client = queue_service_client.get_queue_client(queue=QUEUE_NAME)
    queue_client.create_queue()
except ResourceExistsError:
    pass  # Queue already exists
except Exception as e:
    print(f"Error creating/getting queue: {e}")

# Initialize Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)

# Uploaded container
uploaded_container_client = None
try:
    uploaded_container_client = blob_service_client.get_container_client(UPLOADED_CONTAINER_NAME)
    uploaded_container_client.create_container()
except ResourceExistsError:
    pass  # Already exists
except Exception as e:
    print(f"Error creating/getting uploaded container: {e}")

# Processed container
processed_container_client = None
try:
    processed_container_client = blob_service_client.get_container_client(PROCESSED_CONTAINER_NAME)
    processed_container_client.create_container()
except ResourceExistsError:
    pass  # Already exists
except Exception as e:
    print(f"Error creating/getting processed container: {e}")

@app.route('/', methods=['GET'])
def index():
    uploaded_blobs = []
    processed_blobs = []

    # List blobs in uploaded container
    if uploaded_container_client:
        uploaded_blobs = [
            uploaded_container_client.url + '/' + blob.name
            for blob in uploaded_container_client.list_blobs()
        ]

    # List blobs in processed container
    if processed_container_client:
        processed_blobs = [
            processed_container_client.url + '/' + blob.name
            for blob in processed_container_client.list_blobs()
        ]

    return render_template('index.html', uploaded_blobs=uploaded_blobs, processed_blobs=processed_blobs)

@app.route('/upload', methods=['POST'])
def upload_file():
    if uploaded_container_client is None:
        return "Error: Blob Storage container not initialized.", 500

    if queue_client is None:
        return "Error: Queue client not initialized.", 500

    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        try:
            file_extension = os.path.splitext(file.filename)[1]
            blob_name = f"{uuid4()}{file_extension}"
            uploaded_blob_client = uploaded_container_client.get_blob_client(blob=blob_name)
            uploaded_blob_client.upload_blob(file.read())

            # Create a message for the queue with 30s delay
            message = {"blob_name": blob_name}
            queue_client.send_message(json.dumps(message), visibility_timeout=30)

            return redirect(url_for('index'))

        except Exception as e:
            return f"Error during upload or enqueue: {e}", 500

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

import os
from azure.storage.blob import BlobServiceClient

from ultralytics import YOLO


TARGET_FILE_NAME="bus.jpg"
CONTAINER_NAME="handson-output"
CONNECTION_STRING="<接続文字列>"

def upload_to_blob():
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(container=CONTAINER_NAME)
    with open(f"./runs/detect/predict/{TARGET_FILE_NAME}", "rb") as data:
      container_client.upload_blob(name=TARGET_FILE_NAME, data=data)
    # ファイル削除
    os.remove(f"./runs/detect/predict/{TARGET_FILE_NAME}")

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")
    result = model.predict("bus.jpg", save=True)
    upload_to_blob()
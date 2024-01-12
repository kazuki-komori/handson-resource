import argparse
import zipfile
from azure.storage.blob import BlobServiceClient
import io
import os

# Blob Storage の接続文字列
BLOB_CONNECTION_STRING = os.environ.get("BLOB_CONNECTION_STRING")

def unzip(zip_data: bytes) -> None:
    """unzipは、zipファイルを解凍し、tmpフォルダに展開する関数です。
    Args:
        zip_data (bytes): zipファイルのバイナリデータ
    """
    with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
        zip_ref.extractall("tmp")


def download_file_from_blob(file_name: str) -> bytes:
    """download_file_from_blobは、指定されたファイル名のファイルをダウンロードする関数です。
    Args:
        file_name (str): ダウンロードするファイル名
    Returns:
        bytes: ダウンロードしたファイルのバイナリデータ
    """
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container="zip", blob=file_name)
    
    return blob_client.download_blob().readall()


def upload_unzipped_file2blob() -> None:
    """upload_unzipped_file2blobは、tmpフォルダにあるファイルをBlob Storageにアップロードする関数です。
    """
    for file_name in os.listdir("tmp"):  
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container="unzip", blob=file_name)
        with open(f"./tmp/{file_name}", "rb") as f:
            blob_client.upload_blob(f, overwrite=True)


def main():
    target_zip_file_name = os.environ.get("ZIP_FILE_NAME")

    blob = download_file_from_blob(target_zip_file_name)
    unzip(blob)
    upload_unzipped_file2blob()

if __name__ == '__main__':
    main()
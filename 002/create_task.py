import azure.batch.models as batchmodels
import azure.batch.batch_auth as batchauth
from azure.batch import BatchServiceClient


BATCH_ACCOUNT_ID = '<Batch アカウント ID>'
BATCH_ACCOUNT_KEY = '<Batch アカウント Key>'
BATCH_ACCOUNT_LOCATION = 'japaneast'
BATCH_ACCOUNT_URL = f'https://{BATCH_ACCOUNT_ID}.{BATCH_ACCOUNT_LOCATION}.batch.azure.com'

BATCH_POOL_ID = 'pool-sample-002'
BATCH_JOB_ID = 'job-sample-001'
BATCH_TASK_ID = 'task-sample-001'

BLOB_BATCH_SCRIPT_FILE_NAME = 'sample.py'
BLOB_BATCH_SCRIPT_CONTAINER_NAME = 'handson-input'


def get_batch_client() -> BatchServiceClient:
    """BatchServiceClient インスタンスを取得する"""
    credentials = batchauth.SharedKeyCredentials(
        BATCH_ACCOUNT_ID,
        BATCH_ACCOUNT_KEY
    )
    batch_client = BatchServiceClient(
        credentials,
        batch_url=BATCH_ACCOUNT_URL
    )
    return batch_client

def create_task(batch_client: BatchServiceClient):
    """Batch Task を作成する"""
    task = batchmodels.TaskAddParameter(
        id=BATCH_TASK_ID,
        command_line=f'python {BLOB_BATCH_SCRIPT_FILE_NAME}',
        resource_files=[
            batchmodels.ResourceFile(
                file_path=".",
                auto_storage_container_name=BLOB_BATCH_SCRIPT_CONTAINER_NAME,
            ),
        ]
    )

    batch_client.task.add(job_id=BATCH_JOB_ID, task=task)

if __name__ == "__main__":
    batch_client = get_batch_client()
    create_task(batch_client)
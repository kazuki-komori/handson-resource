import azure.batch.models as batchmodels
import azure.batch.batch_auth as batchauth
from azure.batch import BatchServiceClient


BATCH_ACCOUNT_ID = '<Batch アカウント ID>'
BATCH_ACCOUNT_KEY = '<Batch アカウント Key>'
BATCH_ACCOUNT_LOCATION = 'japaneast'
BATCH_ACCOUNT_URL = f'https://{BATCH_ACCOUNT_ID}.{BATCH_ACCOUNT_LOCATION}.batch.azure.com'

BATCH_POOL_ID = 'pool-sample-001'
BATCH_JOB_ID = 'job-sample-001'

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

def create_job(batch_client: BatchServiceClient):
    """Batch Job を作成する"""
    job = batchmodels.JobAddParameter(
        id=BATCH_JOB_ID,
        pool_info=batchmodels.PoolInformation(pool_id=BATCH_POOL_ID)
    )
    batch_client.job.add(job)

if __name__ == "__main__":
    batch_client = get_batch_client()
    create_job(batch_client)
import azure.batch.models as batchmodels
import azure.batch.batch_auth as batchauth

from azure.batch import BatchServiceClient

BATCH_ACCOUNT_ID = '<Batch アカウント ID>'
BATCH_ACCOUNT_KEY = '<Batch アカウント Key>'
BATCH_ACCOUNT_LOCATION = 'japaneast'
BATCH_ACCOUNT_URL = f'https://{BATCH_ACCOUNT_ID}.{BATCH_ACCOUNT_LOCATION}.batch.azure.com'
BATCH_POOL_ID = 'pool-sample-001'
BATCH_POOL_IMAGE_SIZE = 'Standard_D2S_v3'
BATCH_POOL_VM_COUNT = 2

# 開始タスクで実行するコマンド
BATCH_START_COMMANDS = [
    'apt-get -y update && apt-get -y upgrade',
    "apt-get install -y software-properties-common ffmpeg libsm6 libxext6",
    'add-apt-repository -y ppa:deadsnakes/ppa',
    # python3.10 インストール
    'apt-get install -y python3.10',
    'ln -sfn /usr/bin/python3.10 /usr/bin/python',
    # pip インストール
    'curl -fSsL https://bootstrap.pypa.io/get-pip.py | python',
    "pip install ultralytics==8.0.235",
    "pip install azure-storage-blob==12.19.0",
    "pip install cffi",
]

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

def create_pool(batch_client: BatchServiceClient):
    """Batch Pool を作成する"""
    # 実行権限を付与
    user = batchmodels.AutoUserSpecification(
        scope=batchmodels.AutoUserScope.pool,
        elevation_level=batchmodels.ElevationLevel.admin
    )
    
    pool = batchmodels.PoolAddParameter(
        id=BATCH_POOL_ID,
        virtual_machine_configuration=batchmodels.VirtualMachineConfiguration(
            image_reference=batchmodels.ImageReference(
                publisher='Canonical',
                offer='0001-com-ubuntu-server-focal',
                sku='20_04-lts-gen2',
                version='latest'
            ),
            node_agent_sku_id='batch.node.ubuntu 20.04'
        ),
        vm_size=BATCH_POOL_IMAGE_SIZE,
        target_dedicated_nodes=BATCH_POOL_VM_COUNT,
        start_task=batchmodels.StartTask(
            command_line=(
                f'/bin/bash -c '
                f'\'set -e; set -o pipefail; {";".join(BATCH_START_COMMANDS)}; wait\''
            ),
            user_identity=batchmodels.UserIdentity(auto_user=user),
            wait_for_success=True
        ),
    )

    batch_client.pool.add(pool)

if __name__ == '__main__':
    batch_client = get_batch_client()
    create_pool(batch_client)
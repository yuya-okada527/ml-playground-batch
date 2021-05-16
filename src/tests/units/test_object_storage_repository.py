import os
from pathlib import Path

from infra.repository.object_storage.object_model import ObjectKey
from infra.repository.object_storage.object_storage_repository import \
    LocalStorageRepository


def test_local_storage_save_file(tmp_path):

    # テスト準備
    object_storage_repository = LocalStorageRepository(tmp_path)
    data = "test"
    object_key = ObjectKey(bucket_name="bucket", object_key="dir/file.txt")

    # 実行
    object_storage_repository.save(data.encode("utf-8"), object_key)

    # 検証
    with open(tmp_path / object_key.bucket_name / object_key.object_key, encoding="utf-8") as f:
        assert f.read() == data

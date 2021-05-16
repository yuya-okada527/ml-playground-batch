import os
from pathlib import Path
from typing import Protocol

from infra.repository.object_storage.object_model import ObjectKey

RESOURCE_PATH = Path(__file__).resolve().parents[4] / "resources" / "object_storage"


class ObjectStorageRepository(Protocol):

    def save(self, data: bytes, object_key: ObjectKey) -> None:
        raise NotImplementedError()

    def exists(self, object_key: ObjectKey) -> bool:
        raise NotImplementedError()


class LocalStorageRepository:

    def __init__(self, root_path: Path = RESOURCE_PATH) -> None:
        self.__root_path = root_path

    def save(self, data: bytes, object_key: ObjectKey) -> None:

        # ファイルパスを作成
        file_path = self._make_file_path(object_key)

        # ディレクトリを作成
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # ファイルを保存
        with open(file_path, mode="wb") as f:
            f.write(data)

    def exists(self, object_key: ObjectKey) -> bool:

        # ファイルパスを作成
        file_path = self._make_file_path(object_key)

        # 存在チェック
        return os.path.exists(file_path)

    def _make_file_path(self, object_key: ObjectKey) -> str:
        return self.__root_path / object_key.bucket_name / object_key.object_key


def init_object_storage_repository():
    return LocalStorageRepository()

from pydantic import BaseModel


class ObjectKey(BaseModel):
    """ファイルオブジェクト識別子"""
    bucket_name: str
    object_key: str

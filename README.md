# ML Playground Batch

ML Playground App 用のバッチ処理を提供します。

## 使用技術

- 言語: Python3.9
- フレームワーク: typer
- ORM: sqlalchemy(ORM 部分は未使用)
- ミドルウェア: MySQL, Apache Solr, Redis
- インフラ: Docker
- テストフレームワーク: pytest
- 静的解析ツール: flake8
- 型チェッカー: mypy
- CI ツール: Github Actions
- 主要ライブラリ:
  - requests
  - pydantic
  - redis-py

## 起動方法

```bash
# ローカル起動(Help)
$ python src/app/main.py --help
# 入稿処理
$ sh shells/exec_input.sh
# 出稿処理
$ sh shells/exec_output.sh
# 類似映画データ作成処理
$ sh shells/exec_similarity.sh
# 全実行
$ sh shells/exec_all.sh 0

# コンテナ実行(通常モード)
$ docker-compose run batch sh shells/exec_all.sh 0
```

## 静的解析

```bash
# flake8(1行の文字数制限とビジュアルインデントは無視)
flake8 src/app --ignore E501,E128
```

## デプロイ手順

- main ブランチから release ブランチを作成
- develop ブランチから release ブランチへ PR 作成
- STG 検証
- release ブランチから main ブランチにプッシュ
- 本番反映

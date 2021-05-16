"""メインモジュール

バッチコマンドを定義するモジュール
"""
import typer
from prefect.engine.executors import LocalDaskExecutor

from entrypoints.v1 import (input_entrypoints, output_entrypoints,
                            similarity_entrypoints)
from entrypoints.v2.input.daily_file_tasks import flow as daily_file_flow

# サブコマンドの追加
app = typer.Typer()
app.add_typer(input_entrypoints.app, name="input")
app.add_typer(output_entrypoints.app, name="output")
app.add_typer(similarity_entrypoints.app, name="sim")


if __name__ == "__main__":
    # update_genre_flow()
    daily_file_flow.run(executor=LocalDaskExecutor())

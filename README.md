# Iacta - ダイスを振る Discord Bot

Discord のスラッシュコマンド `/roll` で、ダイス式を評価して結果を返す Bot です。

## 機能

- `/roll` コマンドでダイス式を計算
- 四則演算と括弧に対応
- `d` 演算子でダイスロールに対応（例: `2d6`）
- 指定サーバー（Guild）向けにコマンド同期

## 対応している式

以下の演算子を利用できます。

- 加算: `+`
- 減算: `-`
- 乗算: `*` または `×`
- 除算: `/` または `÷`
- ダイス: `d` または `D`（例: `3d8`）
- 括弧: `(` `)`

優先順位は次の通りです。

1. 括弧
2. `*`, `×`, `/`, `÷`, `d`, `D`
3. `+`, `-`

注意:

- 数値は整数を想定しています。
- 不正な文字や不正な式はエラーメッセージで通知されます。

## セットアップ

### 1. 依存関係のインストール

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

uv を使う場合:

```bash
uv venv
source .venv/bin/activate
uv sync
```

### 2. 環境変数の設定

プロジェクトルートに `.env` を作成し、以下を設定してください。

```dotenv
TOKEN=your_discord_bot_token
SERVER_ID=123456789012345678
```

- `TOKEN`: Discord Bot トークン
- `SERVER_ID`: コマンドを同期する Discord サーバー ID

## 起動方法

```bash
source .venv/bin/activate
python iacta.py
```

uv を使う場合:

```bash
uv run python iacta.py
```

起動後、標準出力に `get on ready!` が表示されれば接続完了です。

## 使い方

Discord で以下のように実行します。

```text
/roll 式:2d6+3
```

レスポンス例:

```text
ユーザー名::`2d6+3` > `((2 d 6) + 3)` > `10`
```

## ディレクトリ構成

```text
.
├── iacta.py            # エントリーポイント
├── cogs/
│   └── roll.py         # /roll コマンド実装
├── modules/
│   └── myast.py        # 式のトークナイズ・構文解析・評価
└── pyproject.toml      # 依存関係などの設定
```

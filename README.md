# AtCoder Problem Solver

AtCoderの問題URLを入力すると、問題をMarkdown化してLLM（Claude AI）に解かせ、C++の解答コードを自動生成するCLIツールです。

## 特徴

- 🔍 AtCoder問題ページの自動スクレイピング
- 📝 問題文のMarkdown形式変換
- 🤖 Claude AIによる自動解答生成（C++17）
- ✅ サンプルケースでの自動検証
- 🔄 検証失敗時の自動リトライ機能

## 必要要件

- Python 3.11以上
- g++ コンパイラ（C++17対応）
- Anthropic API Key

### g++ のインストール

```bash
# Ubuntu/Debian
sudo apt-get install g++

# macOS
xcode-select --install

# 確認
g++ --version
```

## インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/atcoder2markdown.git
cd atcoder2markdown
```

### 2. 依存パッケージのインストール

```bash
pip install -e .
```

または

```bash
pip install -r requirements.txt
```

### 3. API Keyの設定

Anthropic API Keyを環境変数に設定します。

```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集してAPI Keyを設定
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

または直接環境変数として設定:

```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
```

API Keyは [Anthropic Console](https://console.anthropic.com/) から取得できます。

## 使い方

### 基本的な使用方法

```bash
atcoder-solver solve <AtCoder問題URL>
```

例:

```bash
atcoder-solver solve https://atcoder.jp/contests/abc350/tasks/abc350_c
```

### オプション

```bash
atcoder-solver solve <URL> [OPTIONS]

Options:
  -o, --output PATH    出力ディレクトリ（デフォルト: ./output）
  -r, --retry INTEGER  再試行回数（デフォルト: 3）
  -v, --verbose        詳細出力を有効化
  --help               ヘルプを表示
```

### 使用例

```bash
# 詳細出力付きで実行
atcoder-solver solve https://atcoder.jp/contests/abc350/tasks/abc350_c -v

# 出力先を指定
atcoder-solver solve https://atcoder.jp/contests/abc350/tasks/abc350_c -o ./solutions

# 再試行回数を変更
atcoder-solver solve https://atcoder.jp/contests/abc350/tasks/abc350_c -r 5
```

### バージョン確認

```bash
atcoder-solver version
```

## 出力ファイル

実行が成功すると、以下のファイルが出力ディレクトリに生成されます：

```
output/
├── problem.md      # 問題文（Markdown形式）
├── solution.cpp    # 生成された解答コード
└── analysis.md     # 解法説明と計算量分析
```

## アーキテクチャ

### システムフロー

```
[AtCoder問題URL]
    ↓
[1. Scraper] 問題ページをスクレイピング
    ↓
[2. Parser] HTML → Markdown変換
    ↓
[3. Prompt Builder] LLM用プロンプト構築
    ↓
[4. LLM Solver] コード生成（Claude API）
    ↓
[5. Validator] サンプルケースでテスト
    ↓
[6. Output] 解答コード出力
```

### ディレクトリ構成

```
atcoder2markdown/
├── src/
│   ├── __init__.py
│   ├── scraper.py      # 問題取得
│   ├── parser.py       # Markdown変換
│   ├── prompt.py       # プロンプト構築
│   ├── solver.py       # LLM呼び出し
│   ├── validator.py    # テスト実行
│   └── main.py         # CLI エントリポイント
├── templates/          # テンプレートファイル
├── output/             # 生成物出力先
├── tests/              # テストコード
├── pyproject.toml      # プロジェクト設定
├── requirements.txt    # 依存パッケージ
├── .env.example        # 環境変数の例
└── README.md           # このファイル
```

## 技術スタック

| コンポーネント | 技術 |
|--------------|------|
| 言語 | Python 3.11+ |
| スクレイピング | requests, beautifulsoup4 |
| LLM | anthropic (Claude API) |
| CLI | typer |
| コード実行 | subprocess |
| コンパイラ | g++ (C++17) |

## 開発

### 開発環境のセットアップ

```bash
# 開発用依存パッケージのインストール
pip install -e ".[dev]"
```

### テストの実行

```bash
pytest tests/
```

### コードフォーマット

```bash
# Black
black src/

# Ruff
ruff check src/
```

## トラブルシューティング

### g++ が見つからない

```
Error: g++ compiler not found. Please install g++.
```

→ g++コンパイラをインストールしてください（上記「必要要件」を参照）

### API Key が設定されていない

```
ValueError: ANTHROPIC_API_KEY not found in environment variables
```

→ 環境変数 `ANTHROPIC_API_KEY` を設定してください

### コンパイルエラー

生成されたコードがコンパイルエラーになる場合、自動的にリトライされます。
`-r` オプションで再試行回数を増やすことができます。

### サンプルケースが通らない

サンプルケースで不正解になる場合も自動的にリトライされます。
最大試行回数に達した場合でも、生成されたコードは保存されます。

## ライセンス

MIT License

## 貢献

Issue や Pull Request は歓迎します！

## 免責事項

このツールは教育目的で作成されています。
AtCoderの利用規約に従って使用してください。
コンテスト中の使用は禁止されています。

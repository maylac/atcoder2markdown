---
name: atcoder-markdown
description: Converts AtCoder competitive programming problem URLs to Markdown format with structured problem statement, constraints, input/output formats, and sample test cases. Use when the user provides an AtCoder problem URL or asks to solve AtCoder/competitive programming problems. Outputs problem in Markdown for C++ solution generation.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
---

# AtCoder Markdown Converter

AtCoderの競技プログラミング問題をMarkdown形式に変換し、C++解答コード生成を支援するスキルです。

## 使い方

ユーザーがAtCoderの問題URLを提供した場合、このスキルを起動してください。

```bash
cd .claude/skills/atcoder-markdown/scripts
python3 convert.py <AtCoder URL>
```

## 機能

- **自動スクレイピング**: AtCoder問題ページから情報を抽出
- **Markdown変換**: 構造化された読みやすい形式で出力
- **サンプルケース抽出**: 入出力例を自動抽出
- **C++テンプレート提供**: 競技プログラミング用のテンプレート

## 出力内容

### Markdown形式
- 問題タイトル
- 問題文
- 制約条件
- 入力形式
- 出力形式
- サンプルケース（入力・出力ペア）

### オプション
- `--save-samples <file.json>`: サンプルケースをJSONで保存
- `-o <file.md>`: Markdownファイルとして保存

## ワークフロー

1. **問題取得**: URLからAtCoder問題をスクレイピング
2. **Markdown変換**: 構造化されたMarkdown形式で表示
3. **プロンプト生成**: C++競技プログラミング用のシステムプロンプトを読み込み
4. **コード生成**: Claudeが問題とプロンプトを元にC++コードを生成
5. **検証**: ユーザーがサンプルケースで動作確認

## 要件

### Python依存関係
```bash
pip install -r scripts/requirements.txt
```

必要なパッケージ:
- `requests>=2.31.0`: HTTP通信
- `beautifulsoup4>=4.12.0`: HTMLパース

### システム要件
- Python 3.11+
- インターネット接続（AtCoderへのアクセス用）

## テンプレート

### C++テンプレート
[templates/cpp-template.cpp](templates/cpp-template.cpp) を参照

### システムプロンプト
[templates/system-prompt.md](templates/system-prompt.md) を参照

## 使用例

### 例1: 問題のMarkdown変換
```bash
python3 scripts/convert.py https://atcoder.jp/contests/abc350/tasks/abc350_c
```

### 例2: ファイルに保存
```bash
python3 scripts/convert.py https://atcoder.jp/contests/abc350/tasks/abc350_c -o problem.md
```

### 例3: サンプルケースも保存
```bash
python3 scripts/convert.py https://atcoder.jp/contests/abc350/tasks/abc350_c \
  -o problem.md \
  --save-samples samples.json
```

## スキル起動の流れ

1. ユーザーがAtCoder URLを提供
2. このスキルがMarkdown変換を実行
3. 問題Markdownとシステムプロンプトを表示
4. Claudeが問題を分析してC++コードを生成

## トラブルシューティング

### 依存関係エラー
```bash
cd .claude/skills/atcoder-markdown/scripts
pip install -r requirements.txt
```

### スクレイピングエラー
- ネットワーク接続を確認
- AtCoderのURLが正しいか確認
- レート制限の可能性（数秒待って再試行）

詳細は [reference.md](reference.md) を参照してください。

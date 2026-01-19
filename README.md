# AtCoder Markdown Converter

**Claude Code skill for converting AtCoder competitive programming problems to Markdown format**

AtCoderの競技プログラミング問題をMarkdown形式に変換し、Claude AIによるC++解答コード生成を支援するスキルです。

## 特徴

- 🔍 AtCoder問題ページの自動スクレイピング
- 📝 構造化されたMarkdown形式への変換
- 🤖 Claude AIとの統合（C++コード生成支援）
- ✅ サンプルテストケースの自動抽出
- 🎯 競技プログラミング用C++テンプレート提供

## 必要要件

- Python 3.11以上
- インターネット接続（AtCoder アクセス用）
- Claude Code（スキルとして使用する場合）

## インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/atcoder2markdown.git
cd atcoder2markdown
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

または

```bash
cd .claude/skills/atcoder-markdown/scripts
pip install -r requirements.txt
```

### 3. スキルの確認

Claude Codeでリポジトリを開くと、自動的に `.claude/skills/atcoder-markdown/` がスキルとして認識されます。

## 使い方

### Claude Codeでの使用（推奨）

Claude Codeで、AtCoderの問題URLを提供するだけです：

```
ユーザー: この問題を解いてください
https://atcoder.jp/contests/abc350/tasks/abc350_c

Claude: [atcoder-markdownスキルを自動起動]
        問題をMarkdown形式で取得・表示
        解法を分析
        C++コードを生成
```

### スタンドアロン使用

スクリプトを直接実行することも可能です：

```bash
cd .claude/skills/atcoder-markdown/scripts
python3 convert.py https://atcoder.jp/contests/abc350/tasks/abc350_c
```

オプション：
```bash
# Markdownファイルとして保存
python3 convert.py <URL> -o problem.md

# サンプルケースもJSON形式で保存
python3 convert.py <URL> -o problem.md --save-samples samples.json
```

## スキル構成

```
.claude/skills/atcoder-markdown/
├── SKILL.md              # スキル定義（YAML + Markdown）
├── examples.md           # 使用例集
├── reference.md          # 詳細リファレンス
├── scripts/
│   ├── convert.py        # メインスクリプト
│   ├── scraper.py        # スクレイパー
│   ├── parser.py         # Markdown変換
│   └── requirements.txt  # 依存関係
└── templates/
    ├── cpp-template.cpp  # C++テンプレート
    └── system-prompt.md  # システムプロンプト
```

## 出力形式

### Markdown構造

```markdown
# [問題タイトル]

## 問題文
[問題の説明]

## 制約
[制約条件]

## 入力形式
[入力フォーマット]

## 出力形式
[出力フォーマット]

## サンプル

### 入力例1
```
[サンプル入力]
```

### 出力例1
```
[期待される出力]
```
```

## ワークフロー

1. **問題取得**: AtCoder URLから問題をスクレイピング
2. **Markdown変換**: 構造化されたMarkdownに変換
3. **Claude分析**: Claudeが問題を分析
4. **コード生成**: C++17の解答コードを生成
5. **検証**: サンプルケースで動作確認

## C++テンプレート

提供されるC++テンプレート（C++17標準）：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using vi = vector<int>;
using vll = vector<ll>;
#define rep(i, n) for (int i = 0; i < (n); ++i)
#define all(x) (x).begin(), (x).end()

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    // ここに解答コード

    return 0;
}
```

## ドキュメント

- [SKILL.md](.claude/skills/atcoder-markdown/SKILL.md) - スキル定義
- [examples.md](.claude/skills/atcoder-markdown/examples.md) - 使用例集
- [reference.md](.claude/skills/atcoder-markdown/reference.md) - 詳細リファレンス

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

### 依存関係エラー

```bash
cd .claude/skills/atcoder-markdown/scripts
pip install -r requirements.txt
```

### スクレイピングエラー

- ネットワーク接続を確認
- AtCoder URLが正しいか確認
- レート制限の可能性（数秒待って再試行）

### スキルが認識されない

- `.claude/skills/atcoder-markdown/SKILL.md` が存在するか確認
- Claude Codeでリポジトリを再読み込み
- SKILL.mdのYAML frontmatterが正しいか確認

## ライセンス

MIT License

## 貢献

Issue や Pull Request は歓迎します！

## 免責事項

このツールは教育目的で作成されています。
AtCoderの利用規約に従って使用してください。
コンテスト中の使用は禁止されています。

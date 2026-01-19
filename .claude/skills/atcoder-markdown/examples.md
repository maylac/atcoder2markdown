# 使用例

## 例1: 基本的な使用方法

AtCoderの問題URLを提供すると、自動的にMarkdown変換されます。

```
ユーザー: この問題を解いてください
https://atcoder.jp/contests/abc350/tasks/abc350_c

Claude: [atcoder-markdownスキルを起動]
        問題を取得してMarkdown形式で表示
        C++テンプレートとプロンプトを読み込み
        解答コードを生成
```

## 例2: 直接スクリプト実行

```bash
cd .claude/skills/atcoder-markdown/scripts
python3 convert.py https://atcoder.jp/contests/abc350/tasks/abc350_c
```

出力例:
```markdown
# C - New Folder

## 問題文
フォルダ管理システムにおいて...

## 制約
- 1 ≤ N ≤ 10^5

## 入力形式
```
N
A_1 A_2 ... A_N
```

## サンプル

### 入力例1
```
5
3 1 4 1 5
```

### 出力例1
```
3
```
```

## 例3: ファイル保存

```bash
# Markdownとして保存
python3 convert.py https://atcoder.jp/contests/abc350/tasks/abc350_c -o problem.md

# サンプルケースもJSON形式で保存
python3 convert.py https://atcoder.jp/contests/abc350/tasks/abc350_c \
  -o problem.md \
  --save-samples samples.json
```

`samples.json` の内容例:
```json
{
  "problem_title": "C - New Folder",
  "samples": [
    {
      "input": "5\n3 1 4 1 5",
      "output": "3"
    },
    {
      "input": "10\n1 2 3 4 5 6 7 8 9 10",
      "output": "0"
    }
  ]
}
```

## 例4: Claude Codeでの対話的使用

```
ユーザー: AtCoder ABC350のC問題を解いてください
        https://atcoder.jp/contests/abc350/tasks/abc350_c

Claude:
  [Step 1] 問題を取得します
  [atcoder-markdownスキルを起動]

  [Step 2] 問題分析
  # C - New Folder

  ## 問題文
  [取得した問題文]

  [Step 3] 解法説明
  - アルゴリズム: Union-Find
  - 計算量: O(N α(N))
  - アプローチ: [詳細説明]

  [Step 4] C++実装
  ```cpp
  #include <bits/stdc++.h>
  using namespace std;

  // [完全な解答コード]
  ```

  [Step 5] サンプルケースで検証
  入力例1: ✓ 正解
  入力例2: ✓ 正解
```

## 例5: バッチ処理

複数の問題を連続で処理:

```bash
#!/bin/bash

urls=(
  "https://atcoder.jp/contests/abc350/tasks/abc350_a"
  "https://atcoder.jp/contests/abc350/tasks/abc350_b"
  "https://atcoder.jp/contests/abc350/tasks/abc350_c"
)

for url in "${urls[@]}"; do
  problem_id=$(echo $url | grep -oP 'abc\d+_[a-z]')
  python3 convert.py "$url" -o "problems/${problem_id}.md"
done
```

## 例6: C++テンプレートのカスタマイズ

独自のテンプレートを使用:

```bash
# デフォルトテンプレートをコピー
cp templates/cpp-template.cpp my-template.cpp

# カスタマイズ
vim my-template.cpp

# Claudeに「my-template.cppを使って解答を生成してください」と依頼
```

## 例7: エラーハンドリング

無効なURL:
```bash
python3 convert.py https://invalid-url.com
# ✗ Error: Failed to fetch problem: ...
```

ネットワークエラー時:
```bash
python3 convert.py https://atcoder.jp/contests/abc999/tasks/abc999_z
# ✗ Error: Failed to fetch problem: HTTP 404
```

## 例8: CI/CD統合

GitHub Actionsでの使用例:

```yaml
name: Solve AtCoder Problem

on:
  workflow_dispatch:
    inputs:
      problem_url:
        description: 'AtCoder Problem URL'
        required: true

jobs:
  solve:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd .claude/skills/atcoder-markdown/scripts
          pip install -r requirements.txt

      - name: Convert to Markdown
        run: |
          python3 .claude/skills/atcoder-markdown/scripts/convert.py \
            ${{ github.event.inputs.problem_url }} \
            -o problem.md \
            --save-samples samples.json

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: problem-markdown
          path: |
            problem.md
            samples.json
```

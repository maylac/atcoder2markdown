# AtCoder Markdown Converter - リファレンス

## アーキテクチャ

### コンポーネント構成

```
.claude/skills/atcoder-markdown/
├── SKILL.md              # スキル定義（YAML + Markdown）
├── examples.md           # 使用例集
├── reference.md          # このファイル
├── scripts/
│   ├── convert.py        # メインスクリプト
│   ├── scraper.py        # AtCoderスクレイパー
│   ├── parser.py         # Markdown変換
│   └── requirements.txt  # Python依存関係
└── templates/
    ├── cpp-template.cpp  # C++テンプレート
    └── system-prompt.md  # システムプロンプト
```

## API仕様

### convert.py

#### 基本構文
```bash
python3 convert.py <URL> [OPTIONS]
```

#### 引数

| 引数 | 必須 | 説明 | 例 |
|------|-----|------|-----|
| `url` | ✅ | AtCoder問題URL | `https://atcoder.jp/contests/abc350/tasks/abc350_c` |

#### オプション

| オプション | 短縮形 | 説明 | デフォルト |
|-----------|--------|------|-----------|
| `--output` | `-o` | 出力ファイルパス | stdout |
| `--save-samples` | - | サンプルケースのJSON出力先 | なし |

#### 終了コード

| コード | 意味 |
|--------|------|
| 0 | 成功 |
| 1 | エラー（ネットワーク、パース、等） |

#### 標準エラー出力

進捗メッセージは stderr に出力:
```
Fetching problem from <URL>...
✓ Problem fetched: <Title>
✓ Markdown saved to <File>
✓ Samples saved to <File>
```

エラーメッセージ:
```
✗ Error: <Error Message>
```

### scraper.py

#### クラス: AtCoderScraper

```python
class AtCoderScraper:
    def __init__(self, url: str)
    def fetch(self) -> Dict
    def _parse_problem(self) -> Dict
    def _extract_title(self) -> str
    def _extract_sections(self) -> Dict[str, str]
    def _extract_samples(self) -> List[Dict[str, str]]
```

#### 返り値の構造

```python
{
    'title': str,           # 問題タイトル
    'statement': str,       # 問題文
    'constraints': str,     # 制約条件
    'input_format': str,    # 入力形式
    'output_format': str,   # 出力形式
    'samples': [            # サンプルケース
        {
            'input': str,
            'output': str
        },
        ...
    ]
}
```

#### 使用例

```python
from scraper import scrape_problem

problem_data = scrape_problem('https://atcoder.jp/contests/abc350/tasks/abc350_c')
print(problem_data['title'])
# => "C - New Folder"
```

### parser.py

#### クラス: MarkdownParser

```python
class MarkdownParser:
    def __init__(self, problem_data: Dict)
    def to_markdown(self) -> str
```

#### Markdown出力形式

```markdown
# {問題名}

## 問題文
{本文}

## 制約
{制約条件}

## 入力形式
{フォーマット}

## 出力形式
{フォーマット}

## サンプル

### 入力例1
```
{入力}
```

### 出力例1
```
{出力}
```
```

#### 使用例

```python
from scraper import scrape_problem
from parser import parse_to_markdown

problem_data = scrape_problem(url)
markdown = parse_to_markdown(problem_data)
print(markdown)
```

## スキル統合

### Claude Codeでの起動

Claudeが自動的にスキルを検出する条件:

1. **キーワードマッチング**: description内のキーワード
   - "AtCoder"
   - "competitive programming"
   - "problem URL"

2. **URLパターン**: `https://atcoder.jp/contests/.*/tasks/.*`

3. **ユーザーの意図**:
   - "この問題を解いて"
   - "AtCoderのコードを生成"
   - "競技プログラミング"

### スキル実行フロー

```
[ユーザー入力]
    ↓
[Claudeがatcoder-markdownスキルを検出]
    ↓
[convert.pyを実行]
    ↓
[Markdown + System Promptを取得]
    ↓
[Claudeが解答コードを生成]
    ↓
[ユーザーに結果を返す]
```

### システムプロンプトの統合

```python
# templates/system-prompt.md を読み込み
import sys
from pathlib import Path

skill_dir = Path(__file__).parent.parent
system_prompt_path = skill_dir / "templates" / "system-prompt.md"
system_prompt = system_prompt_path.read_text()

# Claudeに渡す
print(system_prompt)
print("\n" + markdown)
```

## 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| なし | - | - |

このスキルは環境変数を使用しません（API keyなどが不要）

## エラーハンドリング

### ネットワークエラー

```python
try:
    problem_data = scrape_problem(url)
except requests.RequestException as e:
    print(f"Network error: {e}")
```

### パースエラー

```python
try:
    problem_data = scrape_problem(url)
except ValueError as e:
    print(f"Parse error: {e}")
```

### タイムアウト

デフォルトタイムアウト: 10秒

変更方法:
```python
# scraper.py内で変更
response = requests.get(self.url, timeout=30)  # 30秒に変更
```

## パフォーマンス

### ベンチマーク

| 処理 | 平均時間 |
|------|---------|
| スクレイピング | 0.5-2秒 |
| Markdown変換 | <0.1秒 |
| 合計 | 0.5-2.1秒 |

### キャッシング

現在実装なし。将来的な拡張:

```python
import hashlib
import json
from pathlib import Path

def get_cache_key(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

def cache_problem(url: str, data: dict):
    cache_dir = Path.home() / ".cache" / "atcoder-markdown"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{get_cache_key(url)}.json"
    cache_file.write_text(json.dumps(data))
```

## カスタマイズ

### C++テンプレートの変更

```cpp
// templates/cpp-template.cpp

// 独自のマクロやtypedefを追加
#define MOD 1000000007
#define INF 1e18

using vi = vector<int>;
using vvi = vector<vi>;
using Graph = vector<vector<int>>;
```

### システムプロンプトの調整

```markdown
<!-- templates/system-prompt.md -->

# カスタムプロンプト

あなたは[特定のスタイル]で回答してください。

## 追加要件
- アルゴリズム名は英語で記述
- 計算量は必ずBig-O記法で
```

### スクレイパーの拡張

他のジャッジサイト対応:

```python
# scripts/scraper.py

class CodeforcesScaper:
    def __init__(self, url: str):
        self.url = url

    def fetch(self) -> Dict:
        # Codeforces固有の実装
        pass
```

## テスト

### ユニットテスト

```python
# tests/test_scraper.py
import pytest
from scripts.scraper import scrape_problem

def test_scrape_problem():
    url = "https://atcoder.jp/contests/abc350/tasks/abc350_c"
    data = scrape_problem(url)
    assert 'title' in data
    assert 'samples' in data
    assert len(data['samples']) > 0
```

### 統合テスト

```bash
#!/bin/bash
# tests/integration_test.sh

python3 scripts/convert.py \
  https://atcoder.jp/contests/abc350/tasks/abc350_c \
  -o /tmp/test.md

if [ -f /tmp/test.md ]; then
  echo "✓ Integration test passed"
else
  echo "✗ Integration test failed"
  exit 1
fi
```

## トラブルシューティング

### よくある問題

#### 1. ImportError: No module named 'requests'

**原因**: 依存関係がインストールされていない

**解決方法**:
```bash
cd .claude/skills/atcoder-markdown/scripts
pip install -r requirements.txt
```

#### 2. UnicodeDecodeError

**原因**: 文字エンコーディングの問題

**解決方法**:
```python
# scraper.py内で明示的にエンコーディング指定
response.encoding = 'utf-8'
```

#### 3. HTTP 404エラー

**原因**: 問題URLが無効

**確認**:
- URLが正しいか確認
- コンテストIDとタスクIDの形式をチェック

#### 4. タイムアウト

**原因**: ネットワークが遅い

**解決方法**:
```python
# scraper.py内でタイムアウトを延長
response = requests.get(self.url, timeout=30)
```

### デバッグ

詳細ログの有効化:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Fetching {url}")
```

## 制限事項

1. **AtCoder専用**: 他のジャッジサイトには未対応
2. **日本語/英語のみ**: 他言語の問題には未対応
3. **静的コンテンツのみ**: JavaScript動的読み込みには未対応
4. **レート制限**: AtCoderのレート制限に従う

## 今後の拡張

- [ ] Codeforces対応
- [ ] LeetCode対応
- [ ] キャッシング機能
- [ ] 複数言語テンプレート（Python, Rust）
- [ ] プロキシ対応
- [ ] ヘッドレスブラウザ対応（Selenium/Playwright）

## ライセンス

MIT License

## 貢献

GitHub: [atcoder2markdown](https://github.com/yourusername/atcoder2markdown)

Issue / Pull Request 歓迎

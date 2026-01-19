"""Prompt builder for LLM solver."""

from typing import Dict


CPP_TEMPLATE = '''#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using vi = vector<int>;
#define rep(i, n) for (int i = 0; i < (n); ++i)
#define all(x) (x).begin(), (x).end()

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    // ここに解答コード

    return 0;
}'''


SYSTEM_PROMPT = """あなたは競技プログラミングの専門家です。

以下のルールに従って、AtCoderの問題を解いてください：

1. C++17標準で解答を生成してください
2. 提供されたテンプレートを使用してください
3. 計算量を意識し、制約を満たすアルゴリズムを選択してください
4. コードの前に簡潔な解法説明を記述してください

## 解答フォーマット

必ず以下の形式で回答してください：

### 解法説明
[ここに解法の説明を記述]
- アルゴリズム: [使用するアルゴリズム名]
- 計算量: [時間計算量と空間計算量]
- ポイント: [実装のポイント]

### C++コード
```cpp
[ここに完全なC++コードを記述]
```

## 重要事項
- コードは必ず完全に動作する状態で提供してください
- 標準入力から読み込み、標準出力に書き込んでください
- エッジケースを考慮してください
- オーバーフローに注意してください（必要に応じてlong longを使用）
"""


class PromptBuilder:
    """Builds prompts for LLM solver."""

    def __init__(self, problem_markdown: str):
        """Initialize prompt builder.

        Args:
            problem_markdown: Problem in Markdown format
        """
        self.problem_markdown = problem_markdown

    def build_system_prompt(self) -> str:
        """Build system prompt for LLM.

        Returns:
            System prompt string
        """
        return SYSTEM_PROMPT

    def build_user_prompt(self) -> str:
        """Build user prompt with problem and template.

        Returns:
            User prompt string
        """
        prompt_parts = [
            "以下の競技プログラミング問題を解いてください。\n",
            "## 問題\n",
            self.problem_markdown,
            "\n## 使用するテンプレート\n",
            "```cpp",
            CPP_TEMPLATE,
            "```\n",
            "上記のテンプレートを使用して、問題を解くC++コードを生成してください。",
        ]

        return '\n'.join(prompt_parts)

    def build_retry_prompt(self, error_message: str, previous_code: str) -> str:
        """Build prompt for retry with error feedback.

        Args:
            error_message: Error message from validator
            previous_code: Previously generated code that failed

        Returns:
            Retry prompt string
        """
        prompt_parts = [
            "以前生成したコードでエラーが発生しました。修正してください。\n",
            "## エラー内容\n",
            "```",
            error_message,
            "```\n",
            "## 以前のコード\n",
            "```cpp",
            previous_code,
            "```\n",
            "エラーを修正した完全なC++コードを再生成してください。",
        ]

        return '\n'.join(prompt_parts)


def build_prompts(problem_markdown: str) -> Dict[str, str]:
    """Convenience function to build prompts.

    Args:
        problem_markdown: Problem in Markdown format

    Returns:
        Dict with 'system' and 'user' keys
    """
    builder = PromptBuilder(problem_markdown)
    return {
        'system': builder.build_system_prompt(),
        'user': builder.build_user_prompt()
    }

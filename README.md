# Pygon宣言

**Python × Go = Pygon** - AI時代の明示的で理解しやすいコーディングスタイル  
**必要環境: Python 3.11以上**

## 概要

**課題**: 生成AI時代の複雑な継承・暗黙的処理、分散チーム開発での説明コスト、マイクロサービスでの不十分なエラーハンドリング

```python
# ❌ 従来Python: エラーケース不明、型注釈不足
def process(items):
    return [transform(x) for x in items if x.is_valid]

# ✅ Pygon: 明示的エラーハンドリングと型注釈
from result import Result, Ok, Err

def process_items(items: list[Item]) -> Result[list[ProcessedItem], str]:
    if not items:
        return Err("validation_error: items required")
    
    result = []
    for item in items:
        if item.is_valid:
            processed_result = transform_item(item)
            if processed_result.is_err():
                return processed_result
            result.append(processed_result.unwrap())
    return Ok(result)
```

## 4つの基本原則

### 1. 明示的エラーハンドリング
例外の代わりに戻り値でエラーを返す。

```python
from result import Result, Ok, Err

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)
```

### 2. シンプルなデータ構造
@dataclass(frozen=True)でデータのみ保持、処理は関数として分離。

```python
@dataclass(frozen=True)
class Task:
    id: int
    title: str
    status: Status
    created_at: str
```

### 3. 単一責任の関数
各関数は一つの明確な責任のみ。小さな関数を組み合わせて複雑な処理を実現。

### 4. 暗黙的動作の排除
すべてを明示的に記述。型注釈、戻り値、エラーケースを明確化。

## Result型パターン

[result](https://github.com/dbrgn/result)ライブラリによる標準的なエラーハンドリング。

```bash
pip install result>=0.16.0
```

```python
from result import Result, Ok, Err

# 基本使用
def divide_safe(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

# パターンマッチング（Python 3.10+）
match divide_safe(10, 0):
    case Ok(value): print(f"Success: {value}")
    case Err(error): print(f"Error: {error}")

# 値の取り出し方法
result = divide_safe(10, 2)
if result.is_ok():
    value = result.unwrap()          # 値を取り出し
    print(f"結果: {value}")
elif result.is_err():
    error = result.unwrap_err()      # エラーを取り出し
    print(f"エラー: {error}")

# チェーン処理
def process_data(raw_data: dict) -> Result[dict, str]:
    return (
        validate_data(raw_data)
        .and_then(lambda _: parse_data(raw_data))
        .and_then(lambda data: normalize_data(data))
    )

# 複雑なチェーンの例
def register_user(form_data: dict) -> Result[User, str]:
    return (
        validate_email(form_data.get("email", ""))
        .and_then(lambda _: validate_user_data(form_data["name"], form_data["email"]))
        .and_then(lambda _: create_user(form_data["name"], form_data["email"]))
    )
```

## 実装要件

### 必須事項
1. **エラーメッセージ**: 「エラータイプ: 詳細」の一貫形式
2. **絶対import**: 相対import禁止（生成AI協調性向上）
3. **型注釈**: すべての関数・変数に型注釈必須
4. **Google形式docstring**: すべての関数・クラスに必須
5. **英語コメント**: 6行に1行程度（17%）の適切な頻度
6. **明示的バリデーション**: すべての入力検証を実装

```python
"""User validation functions for Pygon style programming."""

from src.types.result_types import ValidationResult  # 絶対import

def validate_user_data(user_data: dict) -> ValidationResult:
    # Check email field existence and format
    if "email" not in user_data:
        return False, "validation_error: email is required"
    
    # Validate email format using business rules
    if "@" not in user_data["email"]:
        return False, "validation_error: invalid email format"
    
    return True, None
```

### 非推奨パターン

```python
# ❌ ウォルラス演算子: 可読性低下、AI理解困難
if (result := process_data(input_data)) is not None:
    return result

# ✅ 推奨: 明示的代入
result = process_data(input_data)
if result is not None:
    return result
```

## Docstring規約

Google形式を使用。基本構造：

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """Brief description of what the function does.
    
    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter.
    
    Returns:
        Description of what the function returns.
    
    Example:
        >>> result = function_name("value1", 42)
        >>> print(result)
        Expected output
    """
```

### 実装例

```python
def validate_email(email: str) -> Result[bool, str]:
    """Validate email format using business rules.
    
    Args:
        email: Email address string to validate.
    
    Returns:
        Result[bool, str]: Ok(True) if valid, Err(error_message) if invalid.
    
    Example:
        >>> result = validate_email("user@example.com")
        >>> assert result.is_ok()
    """
    if not email:
        return Err("validation_error: email is required")
    if "@" not in email:
        return Err("validation_error: invalid email format")
    return Ok(True)
```

## 設計指針

### OOP使い分け基準
- **@dataclass**: データ構造（メソッドなし）
- **class**: 状態保持（FileStorage等）
- **function**: ステートレスロジック
- **Protocol**: インターフェース定義

### プロジェクト構成
```
project/
├── src/
│   ├── models/          # @dataclass, Enum
│   ├── validators/      # バリデーション関数
│   ├── services/        # ビジネスロジック関数
│   └── repositories/    # データアクセス関数
├── tests/               # srcと同構造
├── PYGON.md            # スタイルガイド（必須）
└── README.md           # プロジェクト概要
```

### TDD原則
テスト作成 → 最小実装 → リファクタリング（関数分割・責任分離）

## 価値観と適用場面

**核となる価値観**: 明示性 > 簡潔性、予測可能性 > 柔軟性、チーム理解 > 個人効率、長期保守性 > 短期生産性、人間-AI協調

**適用場面**: チーム開発（3名以上）、本番環境、生成AIペアプログラミング、長期保守プロジェクト

**段階的導入**: プロジェクト構成 → エラーハンドリング → 型注釈 → データ構造 → 関数設計 → AI協調最適化

---

**"明示的であることは、暗黙的であることよりも良い"** - The Zen of Python

Pygonは、AI時代の現代的開発環境でこの精神を実現する実践的アプローチ。**誰が読んでもわかる、誰が修正しても安全なコード**を目指す。

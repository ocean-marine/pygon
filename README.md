# Pygon宣言

**Python × Go = Pygon** - 明示的で理解しやすいコーディングスタイル  
**必要環境: Python 3.11以上**

## 課題と背景

**現代開発の課題**: 生成AI時代の複雑な継承・暗黙的処理、分散チーム開発での説明コスト、マイクロサービスでの不十分なエラーハンドリング

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

---

## 基本原則

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

def is_task_overdue(task: Task, current_date: str) -> Result[bool, str]:
    try:
        is_overdue = datetime.fromisoformat(task.created_at) < datetime.fromisoformat(current_date)
        return Ok(is_overdue)
    except ValueError as e:
        return Err(f"date_parse_error: {e}")
```

### 3. 単一責任の関数
各関数は一つの明確な責任のみ。小さな関数を組み合わせて複雑な処理を実現。

```python
from result import Result, Ok, Err

def find_task_by_id(tasks: list[Task], task_id: int) -> Result[Task, str]:
    for task in tasks:
        if task.id == task_id:
            return Ok(task)
    return Err("task_not_found")

def complete_task_workflow(task_id: int) -> Result[Task, str]:
    tasks_result = load_all_tasks()
    if tasks_result.is_err():
        return tasks_result
    
    task_result = find_task_by_id(tasks_result.unwrap(), task_id)
    if task_result.is_err():
        return task_result
    
    updated_task = update_task_status(task_result.unwrap(), Status.COMPLETED)
    return Ok(updated_task)
```

### 4. 暗黙的動作の排除
すべてを明示的に記述。型注釈、戻り値、エラーケースを明確化。

## resultライブラリのサポート

[result](https://github.com/dbrgn/result)ライブラリによる標準的なResult型パターン。

```bash
pip install result>=0.16.0
```

```python
from result import Result, Ok, Err

def divide_with_result(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a / b)

# パターンマッチング（Python 3.10+）
match divide_with_result(10, 0):
    case Ok(value):
        print(f"Success: {value}")
    case Err(error):
        print(f"Error: {error}")

# チェーン処理
def process_user_data(raw_data: dict) -> Result[dict, str]:
    return (
        validate_user_registration(raw_data)
        .and_then(lambda _: parse_user_data(raw_data))
        .and_then(lambda data: normalize_user_data(data))
    )
```

---

## 非推奨記法

### ウォルラス演算子の非推奨化
明示性とAI協調の観点から、以下のパターンは非推奨。

```python
# ❌ ウォルラス演算子: 可読性低下、AIが意図把握困難
if (result := process_data(input_data)) is not None:
    return result

# ✅ 推奨: 明示的代入と変数名
result = process_data(input_data)
if result is not None:
    return result
```

---

## 実践上の重要な注意点

### 必須要件
1. **バリデーション関数**: すべて明示的なバリデーション実装
2. **エラーメッセージ**: 「エラータイプ: 詳細」の一貫形式
3. **絶対import**: 相対import禁止、生成AIとの協調性向上
4. **コメント**: 英語、6行に1行程度（17%）の適切な頻度
5. **ファイル要約**: すべてのPythonファイルにdocstring必須

```python
"""User validation functions for Pygon style programming.

Functions:
    validate_user_data: Validates complete user registration data
    create_user: Creates a new user with validation
"""

from src.types.result_types import ValidationResult  # 絶対import

def validate_user_data(user_data: dict) -> ValidationResult:
    # Check email field existence and format
    if "email" not in user_data:
        return False, "validation_error: email is required"
    
    # Validate email format using business rules
    if "@" not in user_data["email"]:
        return False, "validation_error: invalid email format"
    
    return True, None

def load_config_file(path: str) -> Result[dict, str]:
    try:
        content = Path(path).read_text(encoding="utf-8")
        return Ok(json.loads(content))
    except FileNotFoundError:
        return Err("file_not_found_error: config file does not exist")
    except json.JSONDecodeError as e:
        return Err(f"json_parse_error: {e}")
```

---

## 設計指針

### OOP使い分け基準
- **@dataclass**: データ構造（メソッドなし）
- **class**: 状態保持（FileStorage等）
- **function**: ステートレスロジック
- **Protocol**: インターフェース定義

```python
@dataclass
class User:
    id: int
    name: str
    email: str

class FileStorage:
    def __init__(self, directory: str):
        self.directory = directory
    
    def save_data(self, data: dict) -> Result[bool, str]:
        pass

class Storage(Protocol):
    def save(self, data: dict) -> Result[bool, str]: ...

def validate_email(email: str) -> Result[bool, str]:
    if "@" in email:
        return Ok(True)
    return Err("invalid email")
```

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

### TDD
テスト作成 → 最小実装 → リファクタリング（関数分割・責任分離）

```python
def test_valid_email_returns_success(self):
    result, error = validate_email_format("user@example.com")
    assert error is None and result is True

def test_invalid_email_returns_error(self):
    result, error = validate_email_format("invalid-email")
    assert result is False and "validation_error" in error
```

---

## Pygonの価値観

**核となる価値観**: 明示性 > 簡潔性、予測可能性 > 柔軟性、チーム理解 > 個人効率、長期保守性 > 短期生産性、人間-AI協調

**適用場面**: チーム開発（3名以上）、本番環境、生成AIペアプログラミング、長期保守プロジェクト

**段階的導入**: プロジェクト構成 → エラーハンドリング → 型注釈 → データ構造 → 関数設計 → AI協調最適化

---

**"明示的であることは、暗黙的であることよりも良い"** - The Zen of Python

Pygonは、AI時代の現代的開発環境でこの精神を実現する実践的アプローチ。**誰が読んでもわかる、誰が修正しても安全なコード**を目指す。

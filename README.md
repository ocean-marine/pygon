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
6. **Docstring形式**: Google形式を使用（詳細は以下参照）

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

## Docstring規約 (Google形式)

すべての関数、メソッド、クラスにはGoogle形式のdocstringを記載する。

### Google形式の基本構造

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """Brief description of what the function does.
    
    Longer description if needed. This can span multiple lines
    and provide more detailed information about the function's
    behavior, algorithms, or important notes.
    
    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter.
            Can span multiple lines if needed.
    
    Returns:
        Description of what the function returns.
        Include type information if not obvious from type hints.
    
    Raises:
        ErrorType: Description of when this error is raised.
        AnotherError: Description of another error condition.
    
    Example:
        Basic usage example:
        
        >>> result = function_name("value1", 42)
        >>> print(result)
        Expected output
    
    Note:
        Any additional notes, warnings, or important information.
    """
    pass
```

### Pygon準拠のdocstring例

```python
def validate_email(email: str) -> Result[bool, str]:
    """Validate email format using business rules.
    
    Checks if the provided email address follows basic email format
    requirements including presence of @ symbol and non-empty string.
    
    Args:
        email: Email address string to validate.
    
    Returns:
        Result[bool, str]: Ok(True) if email is valid, 
        Err(error_message) if validation fails.
    
    Example:
        >>> result = validate_email("user@example.com")
        >>> assert result.is_ok()
        
        >>> result = validate_email("invalid-email")
        >>> assert result.is_err()
        >>> print(result.unwrap_err())
        validation_error: invalid email format
    """
    if not email:
        return Err("validation_error: email is required")
    if "@" not in email:
        return Err("validation_error: invalid email format")
    return Ok(True)

@dataclass(frozen=True)
class User:
    """User data model for the application.
    
    Represents a user with basic identification and contact information.
    Uses frozen dataclass to ensure immutability following Pygon principles.
    
    Attributes:
        id: Unique identifier for the user.
        name: Full name of the user.
        email: Email address for the user.
    
    Example:
        >>> user = User(id=1, name="John Doe", email="john@example.com")
        >>> assert user.id == 1
    """
    id: int
    name: str
    email: str

def create_user(name: str, email: str) -> Result[User, str]:
    """Create a new user with validation.
    
    Validates input data and creates a User instance if all validations pass.
    Uses Pygon error handling patterns with explicit Result types.
    
    Args:
        name: Full name of the user. Must be non-empty and <= 50 characters.
        email: Email address. Must be valid email format.
    
    Returns:
        Result[User, str]: Ok(User) if creation successful,
        Err(error_message) if validation fails.
    
    Example:
        >>> result = create_user("John Doe", "john@example.com")
        >>> if result.is_ok():
        ...     user = result.unwrap()
        ...     print(f"Created user: {user.name}")
        
        >>> result = create_user("", "invalid")
        >>> if result.is_err():
        ...     print(f"Error: {result.unwrap_err()}")
        Error: User creation failed: validation_error: name is required
    """
    validation_result = validate_user_data(name, email)
    if validation_result.is_err():
        return validation_result
    
    user = User(id=1, name=name.strip(), email=email.lower())
    return Ok(user)
```

### セクション使用ガイドライン

- **Args**: 必須。すべてのパラメータを記載
- **Returns**: 必須。戻り値の型と意味を明記
- **Raises**: 例外を発生させる場合のみ記載
- **Example**: 複雑な関数には使用例を記載
- **Note**: 重要な注意事項がある場合のみ記載

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

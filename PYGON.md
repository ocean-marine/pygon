# Pygon宣言

**Python × Go = Pygon**

PygonはPythonの柔軟性とGoのシンプルさを融合した、明示的で理解しやすいコーディングスタイルです。

**必要環境: Python 3.11以上**

---

## Pygonが生まれた背景

### 現代開発の3つの課題

#### 1. 生成AIとのペアプログラミング時代
- AIが理解しにくいコード（複雑な継承、暗黙的処理）
- 文脈依存の「Pythonic」な書き方の限界
- 同じ機能でも書き方によるAI生成品質の差

#### 2. リモートワーク・分散チーム開発
- 暗黙の了解に依存したコードの説明コスト
- 新メンバーのオンボーディング困難
- 「書いた人しかわからない」コードのリスク

#### 3. 分散システム・マイクロサービス
- 例外処理だけでは不十分なエラーハンドリング
- 可観測性（ログ・トレーシング）の重要性
- ランタイムエラーの影響拡大

### 従来Pythonの限界

#### 「Pythonic」の功罪
```python
# Pythonic but unclear intent
def process(items):
    return [transform(x) for x in items if validate(x)]

# Hidden error cases
def load_config():
    return json.load(open("config.json"))
```

**問題点：**
- エラーケースが見えない
- 型情報の不足
- 暗黙的な処理への依存

---

## 基本原則

### 1. 明示的エラーハンドリング
例外を投げる代わりに、戻り値でエラーを返す。

```python
def divide(a: int, b: int) -> tuple[float | None, str | None]:
    if b == 0:
        return None, "division by zero"
    return a / b, None

# 使用例
result, err = divide(10, 0)
if err:
    print(f"エラー: {err}")
else:
    print(f"結果: {result}")
```

### 2. 徹底した型注釈
すべての関数に入力・出力の型を明記する。**TypeAliasを活用して複雑な型を分かりやすく命名する。エラー戦略は用途に応じて単一エラーか複数エラーかを使い分ける。**

```python
from dataclasses import dataclass
from typing import TypeAlias, TypeVar

# Define Pygon return value patterns with TypeAlias
T = TypeVar('T')
Result: TypeAlias = tuple[T | None, str | None]
UserResult: TypeAlias = tuple[User | None, str | None]

# Error strategy patterns
SingleValidation: TypeAlias = tuple[bool, str | None]      # Most common: fail fast
MultipleValidation: TypeAlias = tuple[bool, list[str]]     # Forms: collect all errors

@dataclass
class User:
    id: int
    name: str
    email: str

def find_user_by_email(users: list[User], email: str) -> UserResult:
    """Find user by email address.
    
    Args:
        users: List of User objects to search.
        email: Email address to search for.
        
    Returns:
        A tuple of (User object if found, error message if any).
    """
    for user in users:
        if user.email == email:
            return user, None
    return None, "user not found"

# Single error pattern: fail fast (most common)
def validate_email_format(email: str) -> SingleValidation:
    """Validate single field - fail fast approach.
    
    Args:
        email: Email address to validate.
        
    Returns:
        A tuple of (validation result, error message if any).
    """
    if not email:
        return False, "validation_error: email is required"
    if "@" not in email:
        return False, "validation_error: invalid email format"
    return True, None

# Multiple errors pattern: collect all errors for better UX
def validate_user_registration(form_data: dict) -> MultipleValidation:
    """Form validation - collect all errors for user feedback.
    
    Args:
        form_data: Dictionary containing form fields.
        
    Returns:
        A tuple of (validation result, list of error messages).
    """
    errors = []
    
    name = form_data.get("name", "")
    if not name.strip():
        errors.append("validation_error: name is required")
    
    email = form_data.get("email", "")
    if not email or "@" not in email:
        errors.append("validation_error: invalid email format")
    
    age = form_data.get("age", 0)
    if age < 0 or age > 150:
        errors.append("validation_error: age must be between 0 and 150")
    
    return len(errors) == 0, errors

# Generic Result type usage
def parse_json_data(raw_data: str) -> Result[dict]:
    """Parse JSON string to dictionary.
    
    Args:
        raw_data: JSON string to parse.
        
    Returns:
        A tuple of (parsed dictionary if successful, error message if any).
    """
    try:
        data = json.loads(raw_data)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"json_parse_error: {e}"
```

#### エラー戦略の判断基準

**✅ 単一エラー（str | None）を使う場面：**
- 一般的なビジネスロジック（最初のエラーで十分）
- API呼び出し（明確な失敗理由が一つ）
- ファイル・データベース操作（失敗原因は通常一つ）
- パイプライン処理（次の処理に進めない）

**✅ 複数エラー（list[str]）を使う場面：**
- フォームバリデーション（ユーザーが全エラーを知りたい）
- バッチ処理（部分的失敗を許容する場合）
- 設定ファイル検証（複数項目の問題を一度に報告）
- データ移行（どの項目が失敗したか全て必要）

### 3. シンプルなデータ構造
複雑なクラス階層を避け、@dataclassでシンプルな構造体を作る。**データ構造にはメソッドを追加せず、処理は関数として分離する。不変性を保つためfrozen=Trueを推奨。**

```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass(frozen=True)  # Preserve immutability
class Task:
    id: int
    title: str
    status: Status
    created_at: str
    # No methods - data only

# Separate processing as functions
def is_task_overdue(task: Task, current_date: str) -> tuple[bool, str | None]:
    """Check if task is overdue.
    
    Args:
        task: Task object to check.
        current_date: Current date in ISO format.
        
    Returns:
        A tuple of (overdue status, error message if any).
    """
    try:
        task_date = datetime.fromisoformat(task.created_at)
        current = datetime.fromisoformat(current_date)
        return task_date < current, None
    except ValueError as e:
        return False, f"date_parse_error: {e}"

def with_status(task: Task, new_status: Status) -> Task:
    """Create a new Task instance with updated status.
    
    Args:
        task: Original task object.
        new_status: New status to set.
        
    Returns:
        New Task instance with updated status.
    """
    return Task(
        id=task.id,
        title=task.title,
        status=new_status,
        created_at=task.created_at
    )
```

### 4. 単一責任の関数
各関数は一つの明確な責任だけを持つ。**複数の処理を組み合わせる場合は、小さな関数を組み合わせて実現する。**

```python
# ❌ Avoid: Functions with multiple responsibilities
def complete_task(task_id: int) -> tuple[Task | None, str | None]:
    tasks = load_all_tasks()          # Responsibility 1: Data loading
    task = find_task(tasks, task_id)  # Responsibility 2: Task searching
    task.status = Status.COMPLETED   # Responsibility 3: Data modification
    save_all_tasks(tasks)            # Responsibility 4: Data saving
    return task, None

# ✅ Recommended: Combine single-responsibility functions
def find_task_by_id(tasks: list[Task], task_id: int) -> tuple[Task | None, str | None]:
    """Single responsibility: Task searching only.
    
    Args:
        tasks: List of tasks to search.
        task_id: ID of task to find.
        
    Returns:
        A tuple of (found task, error message if any).
    """
    for task in tasks:
        if task.id == task_id:
            return task, None
    return None, "task_not_found"

def update_task_status(task: Task, new_status: Status) -> Task:
    """Single responsibility: Status update only (returns new instance).
    
    Args:
        task: Original task object.
        new_status: New status to set.
        
    Returns:
        New Task instance with updated status.
    """
    return Task(
        id=task.id,
        title=task.title,
        status=new_status,
        created_at=task.created_at
    )

def replace_task_in_list(tasks: list[Task], updated_task: Task) -> list[Task]:
    """Single responsibility: Replace task in list only.
    
    Args:
        tasks: Original list of tasks.
        updated_task: Updated task to replace.
        
    Returns:
        New list with updated task.
    """
    return [updated_task if t.id == updated_task.id else t for t in tasks]

def complete_task_workflow(task_id: int) -> tuple[Task | None, str | None]:
    """Implement functionality by combining small functions.
    
    Args:
        task_id: ID of task to complete.
        
    Returns:
        A tuple of (completed task, error message if any).
    """
    tasks, err = load_all_tasks()
    if err:
        return None, err
    
    task, err = find_task_by_id(tasks, task_id)
    if err:
        return None, err
    
    completed_task = update_task_status(task, Status.COMPLETED)
    updated_tasks = replace_task_in_list(tasks, completed_task)
    
    success, err = save_all_tasks(updated_tasks)
    if err:
        return None, err
    
    return completed_task, None
```

### 5. 暗黙的動作の排除
「魔法的」な動作を避け、すべてを明示的に記述する。

```python
# ❌ Implicit
def process_data(data):
    return transform(data)

# ✅ Explicit
def process_user_data(raw_data: dict[str, str]) -> tuple[User | None, str | None]:
    """Convert raw data to User object.
    
    Args:
        raw_data: Dictionary containing user data.
        
    Returns:
        A tuple of (User object if successful, error message if any).
    """
    if "email" not in raw_data:
        return None, "email field is required"
    
    user = User(
        id=int(raw_data.get("id", 0)),
        name=raw_data.get("name", ""),
        email=raw_data["email"]
    )
    
    return user, None
```

---

## 実践上の重要な注意点

### バリデーション関数の必須化

すべての入力データに対して、専用のバリデーション関数を作成する：

```python
def validate_task_title(title: str) -> tuple[bool, str | None]:
    """Validate task title.
    
    Args:
        title: Task title to validate.
        
    Returns:
        A tuple of (validation result, error message if any).
    """
    if not title:
        return False, "validation_error: title is required"
    
    cleaned_title = title.strip()
    if not cleaned_title:
        return False, "validation_error: title cannot be empty"
    
    if len(cleaned_title) > 100:
        return False, "validation_error: title must be 100 characters or less"
    
    return True, None

def validate_task_id(task_id: int) -> tuple[bool, str | None]:
    """Validate task ID.
    
    Args:
        task_id: Task ID to validate.
        
    Returns:
        A tuple of (validation result, error message if any).
    """
    if task_id <= 0:
        return False, "validation_error: task_id must be positive integer"
    return True, None

# Always validate input in business logic
def create_task(title: str) -> tuple[Task | None, str | None]:
    """Create a new task.
    
    Args:
        title: Title of the task.
        
    Returns:
        A tuple of (created task, error message if any).
    """
    is_valid, err = validate_task_title(title)
    if err:
        return None, err
    
    # Process after validation
    cleaned_title = title.strip()
    # ...
```

### エラーメッセージの一貫性

エラーメッセージは「エラータイプ: 詳細」の形式で統一する：

```python
# ✅ Recommended: Consistent error messages
return None, "validation_error: email format is invalid"
return None, "not_found_error: user not found"
return None, "permission_error: access denied"
return None, f"file_io_error: {e}"

# ❌ Avoid: Inconsistent messages
return None, "invalid email"
return None, "user_not_found"  
return None, "Access denied!"
return None, str(e)
```

### 例外処理の適切な粒度

例外を適切に分類し、それぞれに対応したエラーメッセージを返す：

```python
def load_config_file(path: str) -> tuple[dict | None, str | None]:
    """Load configuration file.
    
    Args:
        path: Path to configuration file.
        
    Returns:
        A tuple of (configuration dictionary, error message if any).
    """
    try:
        content = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, "file_not_found_error: config file does not exist"
    except PermissionError:
        return None, "permission_error: cannot read config file"
    except IOError as e:
        return None, f"file_io_error: {e}"
    
    try:
        data = json.loads(content)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"json_parse_error: invalid JSON format: {e}"
```

---

## Pygonの拡張性・再利用性

### 組み合わせ重視の設計思想

#### 従来のOOP（継承ベース）
```python
# 複雑な継承階層
class Animal:
    def move(self): pass

class Mammal(Animal):
    def breathe(self): pass

class Dog(Mammal):
    def bark(self): pass
```

#### Pygonアプローチ（組み合わせベース）
```python
# Clear separation of responsibilities
@dataclass
class Animal:
    name: str
    species: str

@dataclass 
class MovementCapability:
    can_walk: bool
    can_fly: bool

@dataclass
class Dog:
    animal: Animal
    movement: MovementCapability
    
def make_dog_bark(dog: Dog) -> tuple[str, str | None]:
    """Make dog bark.
    
    Args:
        dog: Dog object to make bark.
        
    Returns:
        A tuple of (bark sound, error message if any).
    """
    if dog.animal.species != "dog":
        return "", "not a dog"
    return f"{dog.animal.name} says woof!", None
```

### プロトコル（Protocol）による柔軟性

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> tuple[str, str | None]: ...

def render_object(obj: Drawable) -> tuple[str, str | None]:
    return obj.draw()
```

---

## 高度なエラーハンドリング

### Go言語から学ぶ「エラーは値」の哲学

#### 構造化エラー（シンプルに）
```python
@dataclass
class PygonError:
    type: str
    message: str
    cause: Exception | None = None

def create_network_error(message: str) -> PygonError:
    return PygonError(type="network_error", message=message)
```

#### エラーラッピング（文脈の追加）
```python
def wrap_error(err: Exception | PygonError, context: str) -> PygonError:
    """エラーに文脈を追加"""
    return PygonError(
        type="wrapped_error",
        message=f"{context}: {err}",
        cause=err
    )
```

#### 複数エラーの蓄積
```python
@dataclass
class MultiError:
    errors: list[PygonError]
    operation: str
    
    def has_errors(self) -> bool:
        return len(self.errors) > 0

def process_multiple_files(files: list[str]) -> tuple[list[str], MultiError | None]:
    """複数ファイル処理（部分的失敗を許容）"""
    processed = []
    multi_err = MultiError([], "file processing")
    
    for file_path in files:
        result, err = process_single_file(file_path)
        if err:
            multi_err.errors.append(wrap_error(err, f"failed: {file_path}"))
            continue
        processed.append(result)
    
    return processed, multi_err if multi_err.has_errors() else None
```

---

## 既存コードとの統合

### デコレータによるPygonスタイル変換

既存の例外ベースコードを、デコレータで簡単にPygonスタイルに変換できます：

```python
from functools import wraps
from typing import Callable, Any

def to_pygon(error_mapping: dict[type, str] | None = None):
    """Convert existing function to Pygon style decorator.
    
    Args:
        error_mapping: Optional mapping from exception types to error messages.
        
    Returns:
        Decorator function that converts exceptions to Pygon-style returns.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> tuple[Any, str | None]:
            try:
                result = func(*args, **kwargs)
                return result, None
            except Exception as e:
                # Use custom error mapping if provided
                if error_mapping:
                    for exc_type, message in error_mapping.items():
                        if isinstance(e, exc_type):
                            return None, f"{message}: {e}"
                
                # Default error mapping
                error_type = type(e).__name__.lower().replace('error', '_error')
                return None, f"{error_type}: {e}"
        
        return wrapper
    return decorator

# Example: Convert existing function
@to_pygon({
    ValueError: "validation_error",
    FileNotFoundError: "file_not_found",
    PermissionError: "permission_denied"
})
def load_config_file(path: str) -> dict:
    """Load configuration file (existing exception-based function).
    
    Args:
        path: Path to configuration file.
        
    Returns:
        Configuration dictionary.
        
    Raises:
        ValueError: If file format is not supported.
        FileNotFoundError: If file does not exist.
    """
    if not path.endswith('.json'):
        raise ValueError("Only JSON files supported")
    
    with open(path) as f:
        return json.load(f)

# Use in Pygon style
config, err = load_config_file("settings.json")
if err:
    print(f"Configuration load failed: {err}")
else:
    print(f"Configuration loaded successfully: {config}")
```

このデコレータにより、既存コードを変更せずに段階的なPygon導入が可能になります。

---

## PygonにおけるOOP使い分け

### ✅ クラスを使うべき場面

#### 1. データ構造の定義（@dataclass）
```python
# ✅ Recommended: Simple data structure (no methods)
@dataclass
class User:
    id: int
    name: str
    email: str
    # No methods - data only

# ❌ Avoid: Adding methods to dataclass
@dataclass
class UserWithMethods:
    id: int
    name: str
    
    def get_display_name(self) -> str:  # ← Should be avoided
        return f"User: {self.name}"

# ✅ Recommended: Separate processing as functions
def get_user_display_name(user: User) -> tuple[str, str | None]:
    """Get user display name.
    
    Args:
        user: User object to get display name for.
        
    Returns:
        A tuple of (display name, error message if any).
    """
    if not user.name.strip():
        return "", "empty_name_error: user name is empty"
    return f"User: {user.name}", None

@dataclass
class DatabaseConfig:
    host: str
    port: int
    password: str
    # Configuration values only
```

#### 2. 状態を保持するコンポーネント
```python
class FileStorage:
    def __init__(self, directory: str):
        self.directory = directory
    
    def save_data(self, data: dict) -> tuple[bool, str | None]:
        """Save data to file.
        
        Args:
            data: Data dictionary to save.
            
        Returns:
            A tuple of (success status, error message if any).
        """
        # Process using directory
        pass
```

#### 3. Protocol（インターフェース）定義
```python
class Storage(Protocol):
    def save(self, data: dict) -> tuple[bool, str | None]: ...
```

### ❌ クラスを避けるべき場面

#### 状態を持たないロジック
```python
# ❌ Unnecessary class creation
class UserValidator:
    def validate_email(self, email: str): ...

# ✅ Simple function
def validate_email(email: str) -> tuple[bool, str | None]:
    """Validate email format.
    
    Args:
        email: Email address to validate.
        
    Returns:
        A tuple of (validation result, error message if any).
    """
    if "@" not in email:
        return False, "invalid email format"
    return True, None
```

### 判断フローチャート
```
Want to define data structure?
├─ Yes → Use @dataclass ✅
└─ No
    └─ Need to hold configuration or state?
        ├─ Yes → Use class ✅
        └─ No → Use function ✅
```

---

## Pygonプロジェクト構成

### 推奨ディレクトリ構造
```
project/
├── src/
│   ├── models/          # Data structures (@dataclass, Enum)
│   │   ├── entities.py  # User, Product etc. entities
│   │   └── errors.py    # ErrorType etc. error definitions
│   │
│   ├── validators/      # Validation function groups
│   │   ├── common.py    # validate_range etc. generic functions
│   │   └── domain.py    # Domain-specific validation
│   │
│   ├── services/        # Business logic function groups
│   │   ├── user.py      # create_user, update_user etc.
│   │   └── payment.py   # process_payment etc.
│   │
│   ├── repositories/    # Data access function groups
│   │   ├── storage.py   # save_to_db, load_from_file etc.
│   │   └── cache.py     # Cache operation functions
│   │
│   ├── protocols/       # Common interface definitions
│   │   └── interfaces.py # Storable, Validatable etc.
│   │
│   ├── config/          # Settings and constants
│   │   ├── settings.py  # @dataclass AppConfig
│   │   └── constants.py # Constant definitions
│   │
│   └── utils/           # Utility functions
│       └── helpers.py   # Generic helper functions
│
├── tests/               # Test code (same structure as src/)
│   ├── unit/            # Unit tests
│   │   ├── test_models/
│   │   ├── test_validators/
│   │   ├── test_services/
│   │   └── test_repositories/
│   │
│   ├── integration/     # Integration tests
│   │   ├── test_workflows/
│   │   └── test_api/
│   │
│   ├── fixtures/        # Test data
│   │   ├── sample_data.json
│   │   └── test_config.py
│   │
│   └── conftest.py      # pytest configuration and shared fixtures
│
├── docs/                # Documentation
├── scripts/             # Operational scripts
├── PYGON.md            # Pygon style guide (this document)
├── README.md           # Project overview and setup
├── TODO.md             # Development tasks and AI collaboration
└── pyproject.toml      # Dependencies and project configuration
```

### プロジェクト文書の役割

#### PYGON.md (必須)
- プロジェクトのルートに配置
- Pygon宣言の最新版をコピー
- プロジェクト固有のパターンや例外事項を追記
- チーム全体とAIツールが参照する統一指針

#### README.md
- プロジェクト概要とクイックスタート
- Pygonスタイルへの言及と PYGON.md への参照
- AI協調開発の説明
- 人間・AI両方が理解できる構成

#### TODO.md  
- 開発タスクとAI協調の記録
- **テンプレートとして提供、自由に改変推奨**
- 個人・チームの作業スタイルに合わせてカスタマイズ
- チェックボックス活用による進捗管理

### TDD（テスト駆動開発）とPygon

PygonはTDDと非常に相性が良く、明示的エラーハンドリングによりテストケースが明確になります。

#### Pygon TDDサイクル
1. **テスト作成** - 期待する戻り値パターンを定義
2. **最小実装** - テストを通す最小限のコード
3. **リファクタリング** - 関数分割・責任分離

#### 基本的なテストパターン

```python
# tests/unit/test_validators/test_email.py
import pytest
from src.validators.email import validate_email_format

class TestEmailValidation:
    """Pygon-style test cases."""
    
    def test_valid_email_returns_success(self):
        """Test that valid email returns success."""
        result, error = validate_email_format("user@example.com")
        
        assert error is None, f"Unexpected error: {error}"
        assert result is True
    
    def test_invalid_email_returns_error(self):
        """Test that invalid email returns error."""
        result, error = validate_email_format("invalid-email")
        
        assert result is False
        assert error is not None
        assert "validation_error" in error
    
    def test_empty_email_returns_error(self):
        """Test that empty string returns error."""
        result, error = validate_email_format("")
        
        assert result is False
        assert error == "validation_error: email cannot be empty"

# tests/unit/test_services/test_user.py
from unittest.mock import patch
from src.services.user import create_user_account
from src.models.entities import User

class TestUserService:
    """Service layer test examples."""
    
    @patch('src.repositories.storage.save_user_to_db')
    @patch('src.validators.email.validate_email_format')
    def test_create_user_success_flow(self, mock_validate, mock_save):
        """Test successful flow."""
        # Setup mocks
        mock_validate.return_value = (True, None)
        mock_save.return_value = (True, None)
        
        # Execute
        user, error = create_user_account("test@example.com", "Test User")
        
        # Verify
        assert error is None
        assert isinstance(user, User)
        assert user.email == "test@example.com"
        
        # Verify mock calls
        mock_validate.assert_called_once_with("test@example.com")
        mock_save.assert_called_once()
    
    @patch('src.validators.email.validate_email_format')
    def test_create_user_validation_failure(self, mock_validate):
        """Test validation failure."""
        # Mock validation failure
        mock_validate.return_value = (False, "validation_error: invalid email")
        
        # Execute
        user, error = create_user_account("invalid-email", "Test User")
        
        # Verify
        assert user is None
        assert error == "validation_error: invalid email"
```

#### テスト作成の指針

**✅ 推奨パターン：**
- 成功ケースと失敗ケースを必ずペアで作成
- エラーメッセージの内容も検証
- モックを使用してサービス層の依存関係を分離

**❌ Avoid patterns:**
- Testing exceptions only (ignoring return value patterns)
- Not validating error messages
- Testing functions with multiple responsibilities

### 構成の設計原則

#### 1. 関数中心の分割
```python
# services/user.py - Business logic
def create_user(email: str, password: str) -> tuple[User | None, str | None]:
    """Create a new user.
    
    Args:
        email: User email address.
        password: User password.
        
    Returns:
        A tuple of (created user, error message if any).
    """
    pass

# validators/user.py - Validation specialized
def validate_user_field(field_name: str, value: str) -> SingleValidation:
    """Validate single user field - fail fast.
    
    Args:
        field_name: Name of the field being validated.
        value: Value to validate.
        
    Returns:
        A tuple of (validation result, error message if any).
    """
    pass

def validate_user_registration_form(form_data: dict) -> MultipleValidation:
    """Validate entire registration form - collect all errors.
    
    Args:
        form_data: Form data dictionary.
        
    Returns:
        A tuple of (validation result, list of error messages).
    """
    pass
```

#### 2. データと処理の分離
```python
# models/ - Pure data structures only
@dataclass
class User:
    id: int
    email: str
    created_at: str
    # No methods at all

# services/ - Functions that manipulate data
def calculate_user_age(user: User, current_date: str) -> tuple[int | None, str | None]:
    """Calculate user age.
    
    Args:
        user: User object to calculate age for.
        current_date: Current date in ISO format.
        
    Returns:
        A tuple of (age in days, error message if any).
    """
    try:
        created = datetime.fromisoformat(user.created_at)
        current = datetime.fromisoformat(current_date)
        age_days = (current - created).days
        return age_days // 365, None
    except ValueError as e:
        return None, f"date_calculation_error: {e}"

def format_user_summary(user: User) -> tuple[str, str | None]:
    """Format user information summary.
    
    Args:
        user: User object to format.
        
    Returns:
        A tuple of (formatted summary, error message if any).
    """
    summary = f"User {user.id}: {user.email}"
    return summary, None
```

---

## Pygonが目指すもの

### 核となる価値観
- **明示性 > 簡潔性** - 短いコードより、わかりやすいコードを
- **予測可能性 > 柔軟性** - 魔法的な動作より、期待通りの動作を
- **チーム理解 > 個人効率** - 一人が書きやすいより、みんなが読みやすいを
- **長期保守性 > 短期生産性** - 今日動くより、来年も安全に変更できるを
- **人間-AI協調 > 人間のみ効率** - AIツールとの効果的な協力を重視

### 適用場面
**推奨：**
- チーム開発（3名以上）
- 本番環境の重要システム
- 生成AIとのペアプログラミング
- 長期保守が予想されるプロジェクト
- 人間-AI混合チームでの開発

**従来Pythonで十分：**
- 個人スクリプト・プロトタイプ
- 一回限りのデータ分析
- 非常に小規模なプロジェクト（100行未満）

### 段階的導入
1. **Phase 1: プロジェクト構成** - PYGON.md、README.md、TODO.mdを配置
2. **Phase 2: エラーハンドリング** - 戻り値でエラーを返すパターン
3. **Phase 3: 型注釈** - TypeAliasと明確な戻り値型
4. **Phase 4: データ構造** - @dataclassでシンプルな構造体
5. **Phase 5: 関数設計** - 単一責任の小さな関数に分割
6. **Phase 6: AI協調最適化** - AIツールとの効率的な協力体制

---

**"明示的であることは、暗黙的であることよりも良い"** - The Zen of Python

Pygonはこの精神を、AI時代の現代的な開発環境で実現するための実践的なアプローチです。

複雑な設計パターンや高度なテクニックよりも、**誰が読んでもわかる、誰が修正しても安全なコード**を目指しましょう。

---

**Pygon Community**  
GitHub: `#pygon-style`  
Discussion: Python開発者のための明示的プログラミング

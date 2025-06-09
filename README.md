# Project Name

Brief description of what this project does and why it exists.

## 🐍 Pygon Style

This project follows **Pygon** coding style - a fusion of Python's flexibility and Go's simplicity for explicit, maintainable code.

> 📋 See [PYGON.md](./PYGON.md) for complete style guidelines and examples.

**Key Pygon principles:**
- Explicit error handling via return values
- TypeAlias for clear return patterns  
- Immutable dataclasses with no methods
- Single-responsibility functions
- Human-AI collaborative development

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- [Additional requirements]

### Installation
```bash
git clone [repository-url]
cd [project-name]
pip install -r requirements.txt
```

### Basic Usage
```python
from src.services.example import process_data

# Pygon-style usage with explicit error handling
result, err = process_data("input_data")
if err:
    print(f"Error: {err}")
    return

print(f"Success: {result}")
```

## 📁 Project Structure

```
project/
├── src/
│   ├── models/          # Data structures (@dataclass, Enum)
│   ├── validators/      # Validation functions
│   ├── services/        # Business logic functions
│   ├── repositories/    # Data access functions
│   ├── protocols/       # Interface definitions
│   ├── config/          # Settings and constants
│   └── utils/           # Utility functions
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── fixtures/       # Test data
├── docs/               # Documentation
├── PYGON.md           # Pygon style guide
├── TODO.md            # Development tasks
└── README.md          # This file
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test category
pytest tests/unit/
pytest tests/integration/
```

## 🤖 AI Collaboration

This project is designed for **human-AI collaborative development**:

- **Clear function signatures** make AI assistance more effective
- **Explicit error handling** reduces AI confusion about edge cases
- **TypeAlias patterns** help AI understand return value expectations
- **Single-responsibility functions** are easier for AI to modify safely

### Working with AI Tools
1. **Copy function signatures** when asking for implementation help
2. **Share error patterns** from existing code for consistency
3. **Reference PYGON.md** when requesting code reviews
4. **Use TODO.md** to track AI-suggested improvements

## 📝 Development Workflow

### Adding New Features
1. **Design data structures** in `src/models/`
2. **Create validation functions** in `src/validators/`
3. **Implement business logic** in `src/services/`
4. **Add tests** following Pygon patterns
5. **Update TODO.md** with progress

### Code Review Checklist
- [ ] All functions have explicit return types
- [ ] Error handling uses `tuple[Result, str | None]` pattern
- [ ] Dataclasses are immutable (`frozen=True`)
- [ ] Single responsibility per function
- [ ] Google-style docstrings
- [ ] English comments only
- [ ] Tests cover both success and error cases

## 🔧 Configuration

[Describe configuration options, environment variables, etc.]

## 📚 API Documentation

[Link to API docs or describe main functions]

## 🤝 Contributing

We welcome contributions! Please:

1. **Follow Pygon style** (see PYGON.md)
2. **Write tests** for new functionality
3. **Update TODO.md** with your changes
4. **Use clear commit messages**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Run type checking
mypy src/

# Run linting
ruff check src/
```

## 📄 License

[License information]

## 📞 Contact

[Contact information or links]

---

**Built with ❤️ using Pygon style**

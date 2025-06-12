# TODO

> 📝 **Template Note**: This is just a starting template. Feel free to modify sections, add new categories, or completely restructure to fit your workflow!

> 🤖 **AI Tip**: Copy relevant sections when working with AI tools.

## 🔥 High Priority

- [ ] Fix user validation bug in `src/validators/user.py`
- [ ] Implement payment processing workflow
- [ ] Update database schema for new user fields
- [ ] Migrate existing code to use rich error handling
- [ ] Add comprehensive tests for PygonError functionality

## 🔄 Medium Priority

- [ ] Refactor legacy functions to Pygon style  
- [ ] Add unit tests for payment module
- [ ] Create user registration form validation
- [ ] Add JSON serialization support for PygonError
- [ ] Create error reporting dashboard using rich error metadata

## 💡 Low Priority / Ideas

- [ ] Add async support to API endpoints
- [ ] Performance optimization for large datasets
- [ ] Add property-based testing
- [ ] Create development setup documentation

## 🤖 AI Collaboration

### AI Suggestions
- [x] Rich error handling with debugging information (implemented by Claude) 
- [ ] Better error categorization (suggested by Claude)
- [ ] Batch processing utilities (suggested by GPT)
- [ ] Add type hints to legacy code (suggested by Copilot)
- [ ] Error pattern analysis using PygonError metadata (suggested by Claude)
- [ ] Automated error recovery strategies (future AI suggestion)

### Need Human Review
- [ ] AI-generated test cases for edge cases
- [ ] Performance impact of recent AI changes
- [ ] Code style consistency after AI refactoring

## 📝 Current Sprint

### In Progress
- [ ] User authentication system (started 2024-01-15)
- [ ] API endpoint documentation
- [ ] Database migration scripts

### This Week
- [ ] Complete user validation
- [ ] Fix critical payment bug
- [ ] Deploy to staging environment
- [ ] Update README with new features

## ✅ Completed

- [x] Set up Pygon project structure
- [x] Created basic validation functions
- [x] Added TypeAlias definitions
- [x] Updated PYGON.md with project specifics
- [x] **Implemented rich error handling system (Issue #5)**
  - [x] Created PygonError class with debugging information
  - [x] Added helper functions for common error types
  - [x] Implemented backward compatibility with legacy string errors
  - [x] Updated examples to demonstrate rich vs legacy patterns
  - [x] Enhanced PYGON.md documentation with rich error patterns
- [x] **Established absolute import policy (Issue #16)**
  - [x] Added comprehensive import policy section to PYGON.md
  - [x] Defined absolute imports as mandatory standard
  - [x] Fixed existing relative import in src/types/__init__.py
  - [x] Documented benefits for AI collaboration and code consistency
- [x] **Defined types module conflict avoidance policy (Issue #18)**
  - [x] Added comprehensive "typesモジュール競合回避方針" section to PYGON.md
  - [x] Established clear guidelines for using src/types/ vs Python's standard types module
  - [x] Created implementation examples and code review checklist
  - [x] Updated README.md code review checklist with types module import requirements
  - [x] Documented AI tool collaboration considerations for types module usage

## 🐛 Bugs

- [ ] Payment validation always returns error
- [ ] User registration form crashes on empty email
- [ ] File upload timeout after 30 seconds
- [ ] Database connection pool exhaustion

## 📚 Learning / Research

- [ ] Study async Pygon patterns
- [ ] Research better testing strategies
- [ ] Explore GraphQL integration
- [ ] Look into containerization options

## 🎯 Goals

### This Month
- [ ] 90% test coverage
- [ ] All functions use Pygon patterns
- [ ] Zero critical bugs
- [ ] Complete user management features

### Next Quarter
- [ ] Performance benchmarks
- [ ] Multi-language support
- [ ] Advanced search features
- [ ] Mobile app integration

---

**Customization Ideas:**
- Add your own priority levels (🚨 Urgent, ⭐ Nice-to-have)
- Create team-specific sections (👥 Team Tasks, 🏠 Remote Work)
- Use different emojis or no emojis at all
- Add time estimates, assignees, or due dates
- Create project-specific categories
- Use whatever structure works best for your workflow!

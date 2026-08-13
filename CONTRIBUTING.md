# Contributing to AI Career Agent

Thank you for your interest in contributing to the AI Career Agent project!

## How to Contribute

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/ai-career-agent.git
cd ai-career-agent
git checkout -b feature/your-feature-name
```

### 2. Set Up Development Environment

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for backend and frontend setup.

### 3. Make Your Changes

**Backend (Python):**
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write tests for new features
- Use `black` for code formatting

**Frontend (JavaScript/TypeScript):**
- Use TypeScript for all new code
- Follow React best practices
- Use Tailwind CSS for styling
- Format with Prettier

### 4. Test Locally

**Backend:**
```bash
cd backend
pytest tests/ -v
```

**Frontend:**
```bash
cd frontend
npm run build  # Check for TypeScript errors
```

### 5. Commit & Push

```bash
git add .
git commit -m "feat: add job fraud detection"
git push origin feature/your-feature-name
```

Use conventional commit messages:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `refactor:` code restructuring
- `test:` adding tests
- `chore:` dependency updates

### 6. Open a Pull Request

Describe:
- What changes you made
- Why the change is needed
- How to test it
- Any breaking changes

## Code Quality

### Backend

```bash
# Format code
black backend/

# Lint
flake8 backend/

# Type check
mypy backend/

# Run tests
pytest backend/ -v --cov
```

### Frontend

```bash
# Format code
npx prettier --write src/

# Lint
npx eslint src/ --fix

# Type check (via build)
npm run build
```

## Reporting Issues

Before opening an issue, check if it's already been reported. Provide:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version, Node version)
- Relevant error messages or logs

## Feature Requests

Describe:
- The use case or problem you're trying to solve
- Proposed solution
- Any alternative approaches
- Impact on users

## Project Structure

Understanding the project layout will help you contribute effectively:

```
backend/
  ├── app/
  │   ├── api/v1/          # Route handlers
  │   ├── core/            # Config and utilities
  │   ├── models/          # Database models
  │   ├── services/        # Business logic
  │   ├── repositories/    # Data access
  │   └── jobs/            # Async tasks
  └── tests/               # Test suite

frontend/
  ├── src/
  │   ├── pages/           # Page components
  │   ├── components/      # Reusable UI components
  │   ├── layouts/         # Layout wrappers
  │   ├── services/        # API client
  │   ├── store/           # Global state
  │   └── hooks/           # Custom React hooks
  └── tests/               # Test suite
```

## Development Tips

### Database Migrations

After changing models, create a migration:

```bash
cd backend
alembic revision --autogenerate -m "Add new field"
alembic upgrade head
```

### API Debugging

Use the Swagger UI at `http://localhost:8000/docs` to test endpoints interactively.

### Frontend Hot Reload

Vite automatically reloads on file changes. No manual refresh needed!

### Environment Variables

Create `.env` files for local testing (excluded from git):

```bash
cp .env.example .env
# Edit .env with your local values
```

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Acknowledge good work

## Questions?

- Open an issue with the `question` label
- Check existing discussions
- Review documentation in [SETUP_GUIDE.md](SETUP_GUIDE.md)

Thank you for contributing to AI Career Agent! 🎉

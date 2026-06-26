# Contributing to Chatbot Platform

We welcome contributions! Please follow these guidelines.

## Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`, `npm test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Standards

### Python
- Follow PEP 8
- Use type hints for all functions
- Write docstrings for public APIs
- Max line length: 100 characters
- Run `ruff check .` before committing

### TypeScript/React
- Follow the project's existing patterns
- Use TypeScript strictly (no `any` where avoidable)
- Use functional components with hooks
- Run `npm run lint` before committing

## Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] CHANGELOG updated if applicable

## Commit Messages

Follow conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `refactor:` code restructuring
- `test:` testing
- `chore:` maintenance

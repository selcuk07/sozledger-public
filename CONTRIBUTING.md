# Contributing to Soz Ledger

Thank you for your interest in contributing to Soz Ledger!

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest features
- Include steps to reproduce for bugs
- Check existing issues before creating a new one

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Add or update tests as needed
5. Ensure all tests pass
6. Submit a pull request

### Development Setup

#### Python SDK

```bash
cd sdk/python
pip install -e ".[dev]"
pytest
```

#### JavaScript SDK

```bash
cd sdk/javascript
npm install
npm test
```

### Code Style

- **Python**: Follow PEP 8. Use type hints.
- **TypeScript**: Follow the existing ESLint configuration.
- **Documentation**: Use Markdown. Keep language clear and concise.

### Protocol Changes

If you're proposing changes to the protocol spec or OpenAPI definition:

1. Open an issue first to discuss the change
2. Update both the OpenAPI spec and relevant JSON schemas
3. Update documentation to reflect the change
4. Ensure backward compatibility or clearly document breaking changes

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

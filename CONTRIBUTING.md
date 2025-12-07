# Contributing to AI Personal Assistant

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 📋 Development Guidelines

### Code Style

#### Python
- Follow PEP 8
- Use type hints
- Write docstrings for functions/classes
- Keep functions small and focused

```python
def process_message(message: str) -> dict:
    """
    Process a user message and return intent data.
    
    Args:
        message: The user's input message
        
    Returns:
        Dictionary containing intent and parameters
    """
    # Implementation
    pass
```

#### TypeScript/React
- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable

```typescript
interface MessageProps {
    content: string;
    role: 'user' | 'assistant';
}

export function Message({ content, role }: MessageProps) {
    // Implementation
}
```

#### CSS
- Use meaningful class names
- Follow BEM naming convention
- Keep selectors specific but not overly complex
- Use CSS variables for theming

### Testing

- Write tests for new features
- Ensure existing tests pass
- Test on multiple browsers (Chrome, Firefox, Safari)
- Test voice input functionality
- Test streaming responses

### Commit Messages

Follow conventional commits:

```
feat: add new integration for Spotify
fix: resolve streaming connection timeout
docs: update API documentation
style: improve glassmorphism effects
refactor: simplify NLU service logic
test: add tests for MCP client
chore: update dependencies
```

## 🏗️ Project Structure

### Adding New MCP Integrations

1. **Create service class** in `mcp-server/app/services/mock_integrations.py`:

```python
class MockNewService:
    def __init__(self):
        self.api_key = settings.NEW_SERVICE_API_KEY
        self.mock_mode = settings.NEW_SERVICE_MOCK_MODE
    
    def action(self, param):
        if self.mock_mode:
            return self._mock_action(param)
        else:
            # Real API implementation
            pass
```

2. **Add configuration** in `mcp-server/app/core/config.py`:

```python
NEW_SERVICE_API_KEY: str = "mock-key"
NEW_SERVICE_MOCK_MODE: bool = True
```

3. **Create router** in `mcp-server/app/routers/integrations.py`:

```python
@router.get("/newservice/action")
async def new_service_action(param: str):
    return new_service.action(param)
```

4. **Update NLU** in `ai-engine/app/services/nlu_service.py`:

```python
if "keyword" in text.lower():
    return {"intent": "new_action", "param": "value"}
```

5. **Document** in DOCUMENTATION.md

### Adding UI Components

1. Create component in `frontend/app/components/`
2. Use TypeScript for props
3. Follow existing styling patterns
4. Add to main Chat component if needed
5. Test responsiveness

## 🧪 Testing Checklist

Before submitting a PR:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No console errors
- [ ] Voice input works
- [ ] Streaming works smoothly
- [ ] UI is responsive
- [ ] Works in Chrome, Firefox, Safari
- [ ] No breaking changes (or documented)

## 📝 Documentation

When adding features:

1. Update DOCUMENTATION.md with technical details
2. Update PROJECT_GUIDE.md if user-facing
3. Add inline code comments
4. Update README.md if needed

## 🔒 Security

- Never commit API keys or secrets
- Use environment variables
- Report security issues privately
- Follow secure coding practices

## 💬 Communication

- Be respectful and constructive
- Ask questions if unclear
- Provide context in discussions
- Help others when possible

## 🎯 Priority Areas

We especially welcome contributions in:

- New MCP integrations
- UI/UX improvements
- Performance optimizations
- Documentation improvements
- Test coverage
- Accessibility features

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution, no matter how small, is valuable and appreciated!

---

**Questions?** Open an issue or start a discussion!

# Welcome

Welcome to the Requirement Loader documentation! This library provides automatic dependency management for Python applications, especially useful for production environments where security updates need to be applied quickly.

## 🚀 What is Requirement Loader?

Requirement Loader is a Python library that automatically fetches and installs Python dependencies from remote sources. It's designed to address security concerns in production environments where zero-day vulnerabilities might be discovered in your dependencies.

### Key Features

- **Remote Requirements Management**: Fetch requirements.txt from URLs or local file (GitHub, HTTP/HTTPS)
- **Automatic Updates**: Continuously monitor for dependency updates
- **Silent Installation**: Install packages without verbose output
- **Application Restart**: Automatically restart your application after updates
- **Flexible Configuration**: Customize update intervals and behavior

### Use Cases

- **Production Security**: Quickly patch zero-day vulnerabilities by updating remote requirements
- **Centralized Dependency Management**: Manage dependencies across multiple deployments from a single source
- **Automated Deployments**: Ensure all instances have the latest approved dependencies

## 📚 Documentation Structure

- **[Installation](installation.md)** - How to install and set up Requirement Loader
- **[Usage](usage.md)** - Complete usage guide with examples and best practices

## 🔧 Quick Start

```python
from requirement_loader import RequirementLoader

# Basic usage with automatic updates
loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
    update_at_startup=True,
    auto_reload=True
)

# Manual update control
manual_loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
    auto_reload=False  # Disable automatic updates
)

# Trigger manual updates when needed
manual_loader.update(reload=True, manual_update=True)
```

## 📝 Version Information

- **Current Version**: 0.0.3
- **Python Compatibility**: 3.11+
- **License**: MIT

## 🤝 Contributing

Found a bug or want to contribute? Visit our [GitHub repository](https://github.com/Ivole32/requirement-loader) to:
- Report issues
- Submit pull requests
- Request features

## 📧 Support

For questions or support, please:
- Open an issue on [GitHub](https://github.com/Ivole32/requirement-loader/issues)
- Contact: ivo.theis@posteo.de
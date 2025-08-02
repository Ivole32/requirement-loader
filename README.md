# 🚀 Requirement Loader

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![PyPI Version](https://img.shields.io/badge/pypi-0.0.3-green.svg)](https://pypi.org/project/requirement-loader/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/Ivole32/requirement-loader.svg)](https://github.com/Ivole32/requirement-loader/issues)

**Automatically fetch and install Python dependencies from remote sources for enhanced security and deployment flexibility.**

When working on production servers, there's always a risk that zero-day vulnerabilities may be discovered in packages listed in your `requirements.txt` file. With Requirement Loader, you can update your requirements file hosted online (e.g., on GitHub) or local, and it will automatically download and install the updated dependencies. The system can either restart your application immediately or defer updates until the next scheduled restart.

## ✨ Key Features

- 🔄 **Automatic Updates**: Continuously monitor and install dependency updates from remote sources
- 🌐 **Multiple Sources**: Support for GitHub, HTTPS/HTTP URLs, and local files
- 🔒 **Security Focused**: Quickly patch zero-day vulnerabilities by updating remote requirements
- ⚡ **Auto Restart**: Automatically restart applications after dependency updates
- 🔇 **Silent Mode**: Install packages without verbose output for clean logs
- ⚙️ **Configurable**: Customize update intervals, restart behavior, and more
- 🐍 **Python 3.11+**: Modern Python support with type hints

## 🚀 Quick Start

### Installation

```bash
pip install requirement-loader
```

### Basic Usage

```python
from requirement_loader import RequirementLoader

# Automatically manage dependencies from GitHub
loader = RequirementLoader(
    requirement_url="https://github.com/yourusername/yourproject/blob/main/requirements.txt",
    update_at_startup=True,
    auto_reload=True,
    sleep_time=300  # Check every 5 minutes
)

# Your application code here
print("Application running with automatic dependency management!")
```

### Advanced Configuration

```python
from requirement_loader import RequirementLoader

# Production setup with custom configuration
loader = RequirementLoader(
    requirement_url="https://your-server.com/secure/requirements.txt",
    update_at_startup=True,      # Install dependencies on startup
    silent_mode=True,            # Quiet installation(s)
    sleep_time=600,              # Check every 10 minutes
    auto_reload=True             # Auto-restart on updates
)
```

## 📖 Documentation

For comprehensive documentation, examples, and best practices, visit our [Wiki](wiki/home.md):

- **[Installation Guide](wiki/installation.md)** - Detailed installation instructions and setup
- **[Usage Guide](wiki/usage.md)** - Complete usage examples and configuration options
- **[Home](wiki/home.md)** - Overview and getting started

## 🛡️ Use Cases

### Production Security
Quickly patch zero-day vulnerabilities by updating your remote requirements file. No need to redeploy - just update the file and let Requirement Loader handle the rest.

```python
# Update requirements.txt on GitHub when a vulnerability is discovered
# Requirement Loader will automatically detect and install the fix
loader = RequirementLoader("https://github.com/company/configs/blob/main/prod-requirements.txt")
```

### Centralized Dependency Management
Manage dependencies across multiple deployments from a single source.

```python
# All your services can use the same requirements source
loader = RequirementLoader("https://internal-repo.company.com/shared-requirements.txt")
```

### Automated Deployments
Ensure all instances have the latest approved dependencies without manual intervention.

```python
# Staging environment with frequent updates
loader = RequirementLoader(
    requirement_url="https://github.com/company/project/blob/staging/requirements.txt",
    sleep_time=60  # Check every minute
)
```

### Manual Updates
For scenarios where you need full control over when updates occur, disable automatic updates and trigger them manually:

```python
from requirement_loader import RequirementLoader

# Disable automatic updates for manual control
loader = RequirementLoader(
    requirement_url="https://github.com/company/project/blob/main/requirements.txt",
    update_at_startup=False,  # Don't update on startup
    auto_reload=False         # Disable background updates
)

# Manually trigger updates when needed
loader.update(reload=True)   # Update and restart application
loader.update(reload=False)  # Update without restarting
```

**Note**: The `manual_update=True` parameter is only available when `auto_reload=False`. This prevents conflicts between automatic and manual update processes.

## 🔧 Supported URL Types

| Type | Example | Description |
|------|---------|-------------|
| **GitHub** | `https://github.com/user/repo/blob/main/requirements.txt` | Automatically converts to raw URL |
| **Raw GitHub** | `https://raw.githubusercontent.com/user/repo/main/requirements.txt` | Direct raw file access |
| **HTTPS** | `https://example.com/requirements.txt` | Any HTTPS URL |
| **HTTP** | `http://internal-server.com/requirements.txt` | HTTP URLs (use with caution) |
| **Local File** | `file:///path/to/requirements.txt` | Local file system |

## ⚙️ Configuration Options

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `requirement_url` | `str` | `"requirements.txt"` | URL or path to requirements file |
| `update_at_startup` | `bool` | `True` | Download and install requirements on initialization |
| `silent_mode` | `bool` | `True` | Install packages without verbose output |
| `sleep_time` | `int` | `5` | Seconds between update checks |
| `auto_reload` | `bool` | `True` | Enable automatic update checking and restart |

### Manual Update Method

```python
loader.update(reload=True, manual_update=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `reload` | `bool` | `False` | Whether to restart the application after update |
| `manual_update` | `bool` | `True` | Must be `True` for manual calls (internal parameter) |

**Important**: `manual_update=True` can only be used when `auto_reload=False` to prevent conflicts.

## 🚨 Error Handling

Requirement Loader includes comprehensive error handling for manual updates:

```python
from requirement_loader import RequirementLoader, ArgumentConflict, RestrictedArgumentError

try:
    # This will work - auto_reload disabled for manual control
    loader = RequirementLoader(
        requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
        auto_reload=False  # Disable automatic updates
    )
    
    # Manual update - this works
    loader.update(reload=True, manual_update=True)
    
except ArgumentConflict as e:
    print(f"Configuration conflict: {e}")
    # This happens when trying manual updates with auto_reload=True
    
except RestrictedArgumentError as e:
    print(f"Invalid argument: {e}")
    # This happens when manual_update=False is used incorrectly
    
except Exception as e:
    print(f"Unexpected error: {e}")

# Example of what causes ArgumentConflict:
try:
    loader_auto = RequirementLoader(auto_reload=True)
    loader_auto.update(manual_update=True)  # This will raise ArgumentConflict
except ArgumentConflict as e:
    print("Can't manually update when auto_reload is enabled!")
```
```

## 🐳 Docker Example

```dockerfile
FROM python:3.11-slim

# Install requirement-loader
RUN pip install requirement-loader

# Copy your application
COPY . /app
WORKDIR /app

# Your app will automatically manage its dependencies
CMD ["python", "app.py"]
```

## 🔒 Security Considerations

- **Use HTTPS URLs** for secure transmission
- **Verify source authenticity** - only use trusted requirement sources
- **Monitor remote files** for unauthorized changes
- **Test updates** in staging before production
- **Implement access controls** on your requirements repositories

## 🧪 Testing

Run the included tests:

```bash
# Clone the repository
git clone https://github.com/Ivole32/requirement-loader.git
cd requirement-loader

# Install development dependencies
pip install -e .

# Run tests
python -m pytest tests/
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/requirement-loader.git
cd requirement-loader

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8
```

## 📋 Requirements

- **Python 3.11+**
- **requests >= 2.25.0**

## 📝 Changelog

### v0.0.3 (Current)
- Initial stable release
- Support for GitHub, HTTPS, HTTP, and local file URLs
- Automatic application restart functionality
- Configurable update intervals
- Silent and verbose installation modes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Ivole32/requirement-loader/issues)
- **Email**: ivo.theis@posteo.de
- **Documentation**: [Wiki](wiki/home.md)

## 🙏 Acknowledgments

- Thanks to all contributors who help make this project better
- Inspired by the need for better dependency management in production environments
- Built with ❤️ for the Python community

---

**⭐ Star this repository if you find it useful!**
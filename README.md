# 🚀 Requirement Loader

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![PyPI Version](https://img.shields.io/badge/pypi-1.0.0-green.svg)](https://pypi.org/project/requirement-loader/)
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
    requirement_temp_file="secure_temp_reqs.txt",  # Custom temporary file
    update_at_startup=True,      # Install dependencies on startup
    silent_mode=True,            # Quiet installation(s)
    sleep_time=600,              # Check every 10 minutes
    auto_reload=True             # Auto-restart on updates
)
```

## 📖 Documentation

For comprehensive documentation, examples, and best practices, visit our [Wiki](https://github.com/Ivole32/requirement-loader/wiki/home):

- **[Installation Guide](https://github.com/Ivole32/requirement-loader/wiki/installation)** - Detailed installation instructions and setup
- **[Usage Guide](https://github.com/Ivole32/requirement-loader/wiki/usage)** - Complete usage examples and configuration options
- **[Home](https://github.com/Ivole32/requirement-loader/wiki/home)** - Overview and getting started

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

### Authentication & Private Repositories
Access private requirements files using custom sessions in manual updates:

```python
import requests
from requirement_loader import RequirementLoader

# Setup loader for private repository (will fail without auth)
loader = RequirementLoader(
    requirement_url="https://github.com/private-org/private-repo/blob/main/requirements.txt",
    auto_reload=False  # Use manual updates for authentication
)

# Create authenticated session
session = requests.Session()
session.headers.update({
    'Authorization': 'token ghp_your_github_token',
    'Accept': 'application/vnd.github.v3.raw'
})

# Update with authentication
loader.update(reload=True, request_session=session)

# Different auth methods for different updates
basic_auth_session = requests.Session()
basic_auth_session.auth = ('username', 'password')
loader.update(reload=False, request_session=basic_auth_session)
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

# Custom authentication for specific updates
import requests
auth_session = requests.Session()
auth_session.headers.update({'Authorization': 'Bearer your-token'})
auth_session.proxies = {'https': 'proxy.company.com:8080'}

# Use custom session for this specific update
loader.update(reload=False, request_session=auth_session)
```

**Note**: When `auto_reload=False`, you have full control over when updates occur and whether to restart the application.

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
| `requirement_temp_file` | `str` | `"requirements_temp.txt"` | Local temporary file path for downloaded requirements |
| `update_at_startup` | `bool` | `True` | Download and install requirements on initialization |
| `silent_mode` | `bool` | `True` | Install packages without verbose output |
| `sleep_time` | `int` | `5` | Seconds between update checks |
| `auto_reload` | `bool` | `True` | Enable automatic update checking and restart |

### Manual Update Method

```python
loader.update(reload=True)   # Update and restart
loader.update(reload=False)  # Update without restart

# With custom session for authentication
import requests
session = requests.Session()
session.auth = ('username', 'password')
loader.update(reload=False, request_session=session)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `reload` | `bool` | `False` | Whether to restart the application after update |
| `request_session` | `requests.Session` | `None` | Custom session for authentication/proxies (optional) |

**Important**: Manual updates are only possible when `auto_reload=False` to prevent conflicts with automatic updates.

## 📁 Temporary File Management

Requirement Loader uses a temporary file to store downloaded requirements before installation. This allows for better control and error handling during the update process.

### Default Behavior

By default, downloaded requirements are saved to `requirements_temp.txt` in your current working directory:

```python
# Uses default temporary file 'requirements_temp.txt'
loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt"
)
```

### Custom Temporary File Location

You can specify a custom location for the temporary requirements file:

```python
# Custom temporary file location
loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
    requirement_temp_file="./temp/my_requirements.txt"  # Custom path
)
```

### Use Cases for Custom Temp Files

```python
# Different environments with separate temp files
if os.environ.get('ENVIRONMENT') == 'production':
    temp_file = "/var/tmp/prod_requirements.txt"
elif os.environ.get('ENVIRONMENT') == 'staging':
    temp_file = "/tmp/staging_requirements.txt"
else:
    temp_file = "dev_requirements_temp.txt"

loader = RequirementLoader(
    requirement_url="https://github.com/company/configs/blob/main/requirements.txt",
    requirement_temp_file=temp_file
)
```

### Security Considerations

- **Temporary files** contain your requirements and should be treated securely
- **File permissions** should be restricted to prevent unauthorized access
- **Cleanup** - temp files are overwritten on each update but not automatically deleted
- **Path traversal** - validate temp file paths to prevent directory traversal attacks

```python
import os

# Secure temporary file handling
def get_secure_temp_path(filename):
    """Ensure temp file is in a secure location"""
    temp_dir = "/secure/temp/path"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, mode=0o700)  # Restricted permissions
    return os.path.join(temp_dir, filename)

loader = RequirementLoader(
    requirement_url="https://private-repo.com/requirements.txt",
    requirement_temp_file=get_secure_temp_path("requirements.txt")
)
```

## 🚨 Error Handling

Requirement Loader defines specific exception types for different error scenarios:

### Exception Types
- **`ArgumentConflict`**: Raised when trying to manually update while `auto_reload=True`
- **`RestrictedArgumentError`**: Raised when attempting to use internal-only parameters

### Error Handling Examples

```python
from requirement_loader import RequirementLoader, ArgumentConflict, RestrictedArgumentError

try:
    # This will work - auto_reload disabled for manual control
    loader = RequirementLoader(
        requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
        auto_reload=False  # Disable automatic updates
    )
    
    # Manual update - this works
    loader.update(reload=True)
    
except ArgumentConflict as e:
    print(f"Configuration conflict: {e}")
    # This happens when trying manual updates with auto_reload=True
    
except RestrictedArgumentError as e:
    print(f"Restricted argument usage: {e}")
    # This happens when trying to use internal-only parameters
    
except Exception as e:
    print(f"Unexpected error: {e}")

# Example of what causes ArgumentConflict:
try:
    loader_auto = RequirementLoader(auto_reload=True)
    loader_auto.update()  # This will raise ArgumentConflict when auto_reload=True
except ArgumentConflict as e:
    print("Can't manually update when auto_reload is enabled!")

# Example of what causes RestrictedArgumentError:
# Note: This would only happen if you try to access internal parameters
# The public API (loader.update(reload=True/False)) doesn't expose these
try:
    loader = RequirementLoader(auto_reload=False)
    # Don't try to use undocumented parameters - they're internal only
    # loader.update(reload=True, manual_update=False)  # This would cause RestrictedArgumentError
except RestrictedArgumentError as e:
    print("Attempted to use internal-only parameter!")
```

## 🐳 Docker Example

```dockerfile
FROM python:3.11-slim

# Install requirement-loader
RUN pip install requirement-loader

# You can use it in your code now
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
```

## 📋 Requirements

- **Python 3.11+**
- **requests >= 2.25.0**

## 📝 Changelog

### v1.0.0 (Current)
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
- **Documentation**: [Wiki](https://github.com/Ivole32/requirement-loader/wiki/home)

## 🙏 Acknowledgments

- Thanks to all contributors who help make this project better
- Inspired by the need for better dependency management in production environments
- Built with ❤️ for the Python community

---

**⭐ Star this repository if you find it useful!**
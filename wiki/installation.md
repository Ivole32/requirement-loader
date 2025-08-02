# Installation Guide

This guide will help you install and set up Requirement Loader in your Python environment.

## 📋 Prerequisites

Before installing Requirement Loader, ensure you have:

- **Python 3.11 or higher**
- **pip** (Python package installer)
- **Internet access** (for downloading packages and remote requirements)

### Check Your Python Version

```bash
python --version
# or
python3 --version
```

## 📦 Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
pip install requirement-loader
```

### Method 2: Install from Source

#### 1. Clone the repository:
```bash
git clone https://github.com/Ivole32/requirement-loader.git
cd requirement-loader
```

#### 2. Install in development mode:
```bash
pip install -e .
```

### Method 3: Install from GitHub

```bash
pip install git+https://github.com/Ivole32/requirement-loader.git
```

## 🔧 Dependencies

Requirement Loader has minimal dependencies:

- **requests** (>=2.25.0) - For HTTP requests to fetch remote requirements

These will be automatically installed when you install the package.

## ✅ Verify Installation

After installation, verify that Requirement Loader is working correctly:

```python
# test_installation.py
from requirement_loader import RequirementLoader

print("Requirement Loader installed successfully!")
print(f"Version: {RequirementLoader.__module__}")
```

## 🐳 Docker Installation

If you're using Docker, add this to your Dockerfile:

```dockerfile
# Install requirement-loader
RUN pip install requirement-loader

# Your application will now have access to RequirementLoader
```

## 🌐 Environment Setup

### Local Development

For local development, you might want to create a virtual environment:

```bash
# Create virtual environment
python -m venv requirement-loader-env

# Activate virtual environment
# On Windows:
requirement-loader-env\Scripts\activate
# On macOS/Linux:
source requirement-loader-env/bin/activate

# Install requirement-loader
pip install requirement-loader
```

### Production Environment

For production deployments:

1. **Create a dedicated requirements file** which will be loaded
2. **Set up proper access controls** for your requirements source
3. **Test the update process** in a staging environment first

## 🚨 Security Setup

### GitHub Token (Optional)

If your requirements file is in a private GitHub repository, you may need to set up authentication:

```python
import os
import requests

# Set up GitHub token for private repositories
headers = {
    'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}',
    'Accept': 'application/vnd.github.v3.raw'
}

# Use with custom requests session if needed
```

### SSL Certificate Verification

Ensure SSL certificates are properly configured for HTTPS requests:

```python
# This is enabled by default, but you can customize if needed
loader = RequirementLoader(
    requirement_url="https://your-secure-server.com/requirements.txt"
    # SSL verification is automatic with requests library
)
```

## 🔍 Troubleshooting

### Common Issues

1. **Python Version Error**
   ```
   ERROR: Package requires a different Python: 3.x.x not in '>=3.11'
   ```
   **Solution**: Upgrade to Python 3.11 or higher

2. **Permission Denied**
   ```
   ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
   ```
   **Solution**: Use `pip install --user requirement-loader` or run with elevated privileges

3. **Network Issues**
   ```
   ERROR: Could not find a version that satisfies the requirement
   ```
   **Solution**: Check your internet connection and proxy settings

4. **Import Error**
   ```
   ModuleNotFoundError: No module named 'requirement_loader'
   ```
   **Solution**: Ensure the package is installed in the correct Python environment

### Getting Help

If you encounter issues during installation:

1. Check the [GitHub Issues](https://github.com/Ivole32/requirement-loader/issues)
2. Create a new issue with:
   - Your Python version
   - Installation method used
   - Complete error message
   - Operating system details

## ⚡ Quick Test

Create a test script to ensure everything is working:

```python
# quick_test.py
from requirement_loader import RequirementLoader
import os

# Create a simple local requirements file for testing
with open("test_requirements.txt", "w") as f:
    f.write("requests>=2.25.0\n")

# Test with automatic updates disabled (for manual control)
loader = RequirementLoader(
    requirement_url="file://test_requirements.txt",
    update_at_startup=False,
    auto_reload=False,
    silent_mode=False
)

print("✅ Requirement Loader is working correctly!")

# Test manual update functionality
print("Testing manual update...")
try:
    loader.update(reload=False)
    print("✅ Manual update functionality works!")
except Exception as e:
    print(f"❌ Manual update failed: {e}")

# Clean up
os.remove("test_requirements.txt")
```

### Testing Manual vs Automatic Updates

```python
# test_update_modes.py
from requirement_loader import RequirementLoader, ArgumentConflict

# Test 1: Manual updates (should work)
try:
    manual_loader = RequirementLoader(
        requirement_url="file://test_requirements.txt",
        auto_reload=False
    )
    manual_loader.update(reload=False)
    print("✅ Manual update mode works correctly")
except Exception as e:
    print(f"❌ Manual update failed: {e}")

# Test 2: Conflict detection (should raise ArgumentConflict)
try:
    auto_loader = RequirementLoader(auto_reload=True)
    auto_loader.update()  # This should fail
    print("❌ Error: Conflict detection not working")
except ArgumentConflict:
    print("✅ Conflict detection works correctly")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

# Test 3: Exception handling test
try:
    from requirement_loader import RestrictedArgumentError
    print("✅ All exception types available")
except ImportError as e:
    print(f"❌ Exception import failed: {e}")
```

## 🎯 Next Steps

Once installation is complete, proceed to the [Usage Guide](usage) to learn how to use Requirement Loader in your applications.
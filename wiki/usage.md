# Usage Guide

This comprehensive guide covers all aspects of using Requirement Loader in your Python applications.

## 📚 Table of Contents

1. [Basic Usage](#-basic-usage)
2. [Configuration Options](#-configuration-options)
3. [URL Types](#-url-types)
4. [Advanced Usage](#-advanced-usage)
5. [Error Handling](#-Error-Handling)
6. [Best Practices](#-best-practices)
7. [Examples](#-examples)

## 🚀 Basic Usage

### Simple Setup

```python
from requirement_loader import RequirementLoader

# Basic setup with GitHub URL
loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
    requirement_temp_file="downloaded_requirements.txt"  # Custom temp file
)
```

This will:
- Download requirements from the specified URL at startup
- Check for updates every 300 seconds (-> 5 minutes)
- Automatically restart your application when updates are found
- Install packages silently

### Manual Control

For complete control over when updates occur, disable automatic updates:

```python
from requirement_loader import RequirementLoader

# Disable automatic updates for manual control
loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
    requirement_temp_file="manual_requirements.txt",  # Custom temp file for manual updates
    update_at_startup=False,
    auto_reload=False
)

# Manually trigger updates when needed
loader.update(reload=True)   # Update and restart application
loader.update(reload=False)  # Update without restarting
```
**Manual updates are forced** which means it will update even when there are no changes.

**Important Note:**
- The manual update function is only available when `auto_reload=False`

## ⚙️ Configuration Options

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `requirement_url` | `str` | `"requirements.txt"` | URL or path to requirements file |
| `requirement_temp_file` | `str` | `"requirements_temp.txt"` | Local temporary file path for downloaded requirements |
| `update_at_startup` | `bool` | `True` | Download and install requirements on initialization |
| `silent_mode` | `bool` | `True` | Install packages without verbose output |
| `sleep_time` | `int` | `300` | Seconds between update checks (when auto_reload=True) |
| `auto_reload` | `bool` | `True` | Enable automatic update checking |

### Manual Update Method

The `update()` method provides manual control over dependency updates:

```python
loader.update(reload=True)   # Update and restart
loader.update(reload=False)  # Update without restart

# With custom session for authentication
import requests
session = requests.Session()
session.headers.update({'Authorization': 'Bearer token'})
loader.update(reload=False, request_session=session)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `reload` | `bool` | `False` | Whether to restart the application after update |
| `request_session` | `requests.Session` | `None` | Custom session for authentication/proxies (optional) |

**Usage Examples:**
```python
# Update without restarting
loader.update(reload=False)

# Update and restart application
loader.update(reload=True)

# Update with authentication
import requests
auth_session = requests.Session()
auth_session.auth = ('username', 'password')
loader.update(reload=False, request_session=auth_session)

# Update with proxy
proxy_session = requests.Session()
proxy_session.proxies = {'https': 'proxy.company.com:8080'}
loader.update(reload=True, request_session=proxy_session)
```

### Example with Custom Configuration

```python
loader = RequirementLoader(
    requirement_url="https://raw.githubusercontent.com/user/repo/main/requirements.txt",
    requirement_temp_file="custom_temp_reqs.txt",  # Custom temporary file
    update_at_startup=True,      # Install on startup
    silent_mode=False,           # Show pip output
    sleep_time=30,               # Check every 30 seconds
    auto_reload=True             # Enable background updates
)
```

### Authentication Examples

```python
import requests
from requirement_loader import RequirementLoader

# Basic loader setup for private resources
loader = RequirementLoader(
    requirement_url="https://private-server.com/requirements.txt",
    auto_reload=False  # Use manual updates for authentication
)

# GitHub Personal Access Token
github_session = requests.Session()
github_session.headers.update({
    'Authorization': 'token ghp_your_github_token',
    'Accept': 'application/vnd.github.v3.raw'
})
loader.update(reload=False, request_session=github_session)

# Basic Authentication
basic_session = requests.Session()
basic_session.auth = ('username', 'password')
loader.update(reload=False, request_session=basic_session)

# API Key Authentication
api_session = requests.Session()
api_session.headers.update({'X-API-Key': 'your-api-key'})
loader.update(reload=False, request_session=api_session)

# Proxy with Authentication
proxy_session = requests.Session()
proxy_session.proxies = {
    'http': 'http://user:pass@proxy.company.com:8080',
    'https': 'https://user:pass@proxy.company.com:8080'
}
loader.update(reload=False, request_session=proxy_session)

# SSL Certificate Configuration
ssl_session = requests.Session()
ssl_session.verify = '/path/to/ca-bundle.crt'
ssl_session.cert = ('/path/to/client.cert', '/path/to/client.key')
loader.update(reload=False, request_session=ssl_session)
```

## 🌐 URL Types

### GitHub URLs

Requirement Loader automatically converts GitHub blob URLs to raw URLs:

```python
# These are equivalent:
loader1 = RequirementLoader("https://github.com/user/repo/blob/main/requirements.txt")
loader2 = RequirementLoader("https://raw.githubusercontent.com/user/repo/main/requirements.txt")
```

### HTTPS URLs

Any HTTPS URL pointing to a text file:

```python
loader = RequirementLoader("https://example.com/path/to/requirements.txt")
```

### HTTP URLs

```python
loader = RequirementLoader("http://internal-server.com/requirements.txt")
```

### Local Files

Use file:// protocol for local files:

```python
loader = RequirementLoader("file:///path/to/local/requirements.txt")
# or
loader = RequirementLoader("file://./requirements.txt")
```

## � Temporary File Management

Requirement Loader downloads requirements to a temporary file before installation. This provides better control over the update process and allows for validation before installation.

### Default Temporary File

By default, requirements are saved to `requirements_temp.txt`:

```python
# Uses default temp file 'requirements_temp.txt'
loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt"
)
```

The temporary file will be created in your current working directory and will contain the downloaded requirements content.

### Custom Temporary File Path

You can specify a custom location for the temporary requirements file:

```python
# Custom temporary file location
loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
    requirement_temp_file="./temp/project_requirements.txt"
)
```

### Environment-Specific Temporary Files

```python
import os

# Different temp files for different environments
def get_temp_file_path():
    env = os.environ.get('ENVIRONMENT', 'development')
    
    if env == 'production':
        return "/var/app/temp/prod_requirements.txt"
    elif env == 'staging':
        return "/tmp/staging_requirements.txt"
    else:
        return "dev_requirements_temp.txt"

loader = RequirementLoader(
    requirement_url="https://github.com/company/project/blob/main/requirements.txt",
    requirement_temp_file=get_temp_file_path(),
    auto_reload=True
)
```

### Temporary File in Secure Directory

```python
import os
import tempfile

# Create temporary file in system temp directory
temp_dir = tempfile.gettempdir()
temp_file = os.path.join(temp_dir, "secure_requirements.txt")

loader = RequirementLoader(
    requirement_url="https://private-repo.com/requirements.txt",
    requirement_temp_file=temp_file
)
```

### Advanced Temporary File Handling

```python
import os
from pathlib import Path

class SecureRequirementLoader:
    def __init__(self, requirement_url, temp_dir="./temp"):
        # Ensure temp directory exists
        Path(temp_dir).mkdir(parents=True, exist_ok=True)
        
        # Set secure permissions (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            os.chmod(temp_dir, 0o700)
        
        temp_file = os.path.join(temp_dir, "requirements_secure.txt")
        
        self.loader = RequirementLoader(
            requirement_url=requirement_url,
            requirement_temp_file=temp_file,
            auto_reload=False
        )
    
    def secure_update(self):
        """Update with additional security checks"""
        try:
            # Perform update
            self.loader.update(reload=False)
            
            # Validate temp file contents
            if self._validate_requirements():
                print("Requirements validated successfully")
                self.loader.update(reload=True)
            else:
                print("Requirements validation failed")
                
        except Exception as e:
            print(f"Secure update failed: {e}")
    
    def _validate_requirements(self):
        """Validate requirements file content"""
        try:
            with open(self.loader.requirement_temp_file, 'r') as f:
                content = f.read()
                
            # Basic validation - check for suspicious content
            suspicious_patterns = ['rm -rf', 'sudo', 'curl', 'wget']
            for pattern in suspicious_patterns:
                if pattern in content.lower():
                    return False
                    
            # Check if it looks like a valid requirements file
            lines = content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Should contain package names or version specs
                    if not any(c.isalnum() for c in line):
                        return False
                        
            return True
            
        except Exception:
            return False

# Usage
secure_loader = SecureRequirementLoader(
    "https://github.com/trusted/repo/blob/main/requirements.txt"
)
secure_loader.secure_update()
```

### Temporary File Lifecycle

1. **Download**: Requirements are fetched from the URL
2. **Compare**: New content is compared with existing temp file
3. **Write**: If different, new content overwrites the temp file
4. **Install**: pip installs from the temp file
5. **Persist**: Temp file remains for next comparison

### Best Practices for Temporary Files

```python
import os
import tempfile
from pathlib import Path

# 1. Use absolute paths to avoid confusion
temp_file = os.path.abspath("./temp/requirements.txt")

# 2. Ensure directory exists
Path(temp_file).parent.mkdir(parents=True, exist_ok=True)

# 3. Use platform-appropriate temp directories
if os.name == 'nt':  # Windows
    temp_file = os.path.join(os.environ['TEMP'], 'app_requirements.txt')
else:  # Unix-like
    temp_file = '/tmp/app_requirements.txt'

# 4. Include project identifier in filename
project_name = "myapp"
temp_file = f"/tmp/{project_name}_requirements.txt"

loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
    requirement_temp_file=temp_file
)
```

### Troubleshooting Temporary Files

```python
import os
from requirement_loader import RequirementLoader

def debug_temp_file(loader):
    """Debug temporary file issues"""
    temp_file = loader.requirement_temp_file
    
    print(f"Temporary file path: {temp_file}")
    print(f"Temp file exists: {os.path.exists(temp_file)}")
    
    if os.path.exists(temp_file):
        print(f"File size: {os.path.getsize(temp_file)} bytes")
        print(f"File readable: {os.access(temp_file, os.R_OK)}")
        print(f"File writable: {os.access(temp_file, os.W_OK)}")
        
        # Show first few lines of temp file
        try:
            with open(temp_file, 'r') as f:
                content = f.read()
                lines = content.split('\n')[:5]
                print("First 5 lines:")
                for i, line in enumerate(lines, 1):
                    print(f"  {i}: {line}")
        except Exception as e:
            print(f"Cannot read temp file: {e}")
    
    # Check directory permissions
    temp_dir = os.path.dirname(temp_file)
    print(f"Directory exists: {os.path.exists(temp_dir)}")
    print(f"Directory writable: {os.access(temp_dir, os.W_OK)}")

# Usage
loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
    requirement_temp_file="./debug/requirements.txt",
    auto_reload=False
)

debug_temp_file(loader)
```

The temporary file feature provides flexibility and control over where downloaded requirements are stored, enabling better integration with different deployment environments and security requirements.

## �🔥 Advanced Usage

### Manual Update Strategies

When you need precise control over update timing, use manual updates:

```python
from requirement_loader import RequirementLoader
import time
import datetime

class ManualUpdateController:
    def __init__(self, requirement_url):
        # Always disable auto_reload for manual control
        self.loader = RequirementLoader(
            requirement_url=requirement_url,
            auto_reload=False,
            update_at_startup=False  # Don't update on initialization
        )
        
    def check_and_update(self, force_restart=True):
        """Manually check for updates and optionally restart"""
        try:
            print(f"Checking for updates at {datetime.datetime.now()}")
            
            # Check for updates without restarting
            self.loader.load_requirements()
            
            if self.loader.new_version:
                print("New requirements detected!")
                
                if force_restart:
                    print("Restarting application...")
                    self.loader.update(reload=True)
                else:
                    self.loader.update(reload=False)
                    print("Update installed, restart manually when ready")
                    
            else:
                print("No updates available")
                
        except Exception as e:
            print(f"Update failed: {e}")
    
    def force_update(self):
        """Force update even if requirements haven't changed"""
        print("Forcing update...")
        self.loader.update(reload=True)
    
    def update_without_restart(self):
        """Update packages but don't restart application"""
        print("Updating packages without restart...")
        self.loader.update(reload=False)

# Usage examples
controller = ManualUpdateController(
    "https://github.com/user/repo/blob/main/requirements.txt"
)

# Check for updates and restart if needed
controller.check_and_update(force_restart=True)

# Update without restarting
controller.update_without_restart()

# Force update regardless of changes
controller.force_update()
```

### Background Updates with Custom Logic

```python
from requirement_loader import RequirementLoader
import time

class CustomRequirementLoader:
    def __init__(self):
        # Disable auto-reload to handle updates manually
        self.loader = RequirementLoader(
            requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
            auto_reload=False,
            silent_mode=False
        )
        
    def start_custom_update_cycle(self):
        while True:
            try:
                print("Checking for updates...")
                # Use manual update for precise control
                self.loader.update(reload=False)
                
                # Custom logic here - e.g., send notifications, log updates
                if self.loader.new_version:
                    print("New version detected! Scheduling restart...")
                    # Perform cleanup, save state, etc.
                    time.sleep(5)  # Grace period
                    # Restart with manual update
                    self.loader.update(reload=True)
                    
            except Exception as e:
                print(f"Update check failed: {e}")
                
            time.sleep(60)  # Check every minute

# Usage
custom_loader = CustomRequirementLoader()
custom_loader.start_custom_update_cycle()
```

### Conditional Updates

```python
from requirement_loader import RequirementLoader
import datetime

class ScheduledRequirementLoader:
    def __init__(self):
        self.loader = RequirementLoader(
            requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
            auto_reload=False,
            update_at_startup=False
        )
        
    def update_during_maintenance_window(self):
        """Only update during specific hours"""
        current_hour = datetime.datetime.now().hour
        
        # Maintenance window: 2 AM - 4 AM
        if 2 <= current_hour <= 4:
            print("In maintenance window, checking for updates...")
            self.loader.update(reload=True)
        else:
            print("Outside maintenance window, skipping update")

# Usage
scheduled_loader = ScheduledRequirementLoader()
```

### Multiple Requirement Sources

```python
from requirement_loader import RequirementLoader

class MultiSourceLoader:
    def __init__(self):
        self.loaders = [
            RequirementLoader(
                requirement_url="https://github.com/user/repo/blob/main/base_requirements.txt",
                auto_reload=False
            ),
            RequirementLoader(
                requirement_url="https://github.com/user/repo/blob/main/security_requirements.txt",
                auto_reload=False
            )
        ]
    
    def update_all_sources(self):
        for i, loader in enumerate(self.loaders):
            print(f"Updating source {i+1}...")
            loader.update(reload=False)
        
        # Restart only after all updates
        print("All sources updated, restarting...")
        self.loaders[0]._reload_program()

# Usage
multi_loader = MultiSourceLoader()
```

## 🚨 Error Handling

### Exception Types

Requirement Loader defines two specific exception types:

#### ArgumentConflict
Raised when there's a conflict between automatic and manual update modes:
- **When it occurs**: Trying to call `update()` when `auto_reload=True`
- **Solution**: Set `auto_reload=False` for manual control

#### RestrictedArgumentError  
Raised when trying to access internal-only functionality:
- **When it occurs**: Attempting to use undocumented internal parameters
- **Solution**: Use only the public API methods

### Understanding Exceptions

Requirement Loader has specific error handling for manual updates:

```python
from requirement_loader import RequirementLoader, ArgumentConflict, RestrictedArgumentError

try:
    # Correct setup for manual updates
    loader = RequirementLoader(auto_reload=False)  # Disable auto updates
    
    # This will work
    loader.update(reload=True)
    
except ArgumentConflict as e:
    print(f"Configuration conflict: {e}")
    # This happens when trying to manually update with auto_reload=True
    
except RestrictedArgumentError as e:
    print(f"Restricted argument usage: {e}")
    # This happens when trying to access internal-only parameters
    
except Exception as e:
    print(f"Unexpected error: {e}")

# Common error scenarios:
try:
    # This will raise ArgumentConflict
    auto_loader = RequirementLoader(auto_reload=True)
    auto_loader.update()  # ERROR: Can't manually update when auto_reload=True
    
except ArgumentConflict as e:
    print("Cannot manually update when auto_reload is enabled!")

# RestrictedArgumentError example:
# This error occurs when trying to use internal-only parameters
# The public API doesn't expose these, but it's good to know about this error
try:
    loader = RequirementLoader(auto_reload=False)
    # The following would cause RestrictedArgumentError if attempted:
    # loader.update(reload=True, manual_update=False)  # Internal parameter only
    print("Using public API only - no issues!")
    
except RestrictedArgumentError as e:
    print("Attempted to use internal-only functionality!")
```

### Robust Error Handling

```python
from requirement_loader import RequirementLoader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustRequirementLoader:
    def __init__(self, requirement_url):
        self.requirement_url = requirement_url
        self.loader = None
        self.setup_loader()
    
    def setup_loader(self):
        try:
            self.loader = RequirementLoader(
                requirement_url=self.requirement_url,
                auto_reload=False,  # Handle updates manually
                silent_mode=True
            )
            logger.info("RequirementLoader initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RequirementLoader: {e}")
            # Fallback to local requirements
            self.loader = RequirementLoader(
                requirement_url="file://requirements.txt",
                auto_reload=False
            )
    
    def safe_update(self):
        if not self.loader:
            logger.error("Loader not initialized")
            return False
            
        try:
            self.loader.update(reload=False)
            logger.info("Update completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Update failed: {e}")
            return False

# Usage
robust_loader = RobustRequirementLoader(
    "https://github.com/user/repo/blob/main/requirements.txt"
)
```

## 💡 Best Practices

### 1. Production Setup

```python
# production_loader.py
import os
from requirement_loader import RequirementLoader

# Use environment variables for configuration
REQUIREMENTS_URL = os.environ.get(
    'REQUIREMENTS_URL', 
    'https://github.com/company/configs/blob/main/production_requirements.txt'
)

UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', 300))  # 5 minutes
TEMP_FILE_PATH = os.environ.get('TEMP_FILE_PATH', 'prod_requirements_temp.txt')

loader = RequirementLoader(
    requirement_url=REQUIREMENTS_URL,
    requirement_temp_file=TEMP_FILE_PATH,  # Environment-configurable temp file
    update_at_startup=True,
    silent_mode=True,
    sleep_time=UPDATE_INTERVAL,
    auto_reload=True
)
```

### 2. Graceful Shutdown

```python
import signal
import sys
from requirement_loader import RequirementLoader

class GracefulRequirementLoader:
    def __init__(self):
        self.loader = RequirementLoader(auto_reload=False)
        self.running = True
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        print('Gracefully shutting down...')
        self.running = False
        # Perform cleanup
        sys.exit(0)
    
    def run(self):
        while self.running:
            try:
                self.loader.update(reload=False)
                time.sleep(60)
            except KeyboardInterrupt:
                break

# Usage
graceful_loader = GracefulRequirementLoader()
graceful_loader.run()
```

### 3. Development vs Production

```python
import os
from requirement_loader import RequirementLoader

# Different configurations for different environments
if os.environ.get('ENVIRONMENT') == 'production':
    loader = RequirementLoader(
        requirement_url="https://github.com/company/configs/blob/main/prod_requirements.txt",
        sleep_time=300,  # 5 minutes
        silent_mode=True
    )
elif os.environ.get('ENVIRONMENT') == 'staging':
    loader = RequirementLoader(
        requirement_url="https://github.com/company/configs/blob/main/staging_requirements.txt",
        sleep_time=60,   # 1 minute
        silent_mode=False
    )
else:  # development
    loader = RequirementLoader(
        requirement_url="file://dev_requirements.txt",
        auto_reload=False,  # Manual updates in dev
        silent_mode=False
    )
```

## 📝 Examples

### Example 1: Flask Web Application

```python
# app.py
from flask import Flask, jsonify
from requirement_loader import RequirementLoader
import threading

app = Flask(__name__)

# Initialize requirement loader
loader = RequirementLoader(
    requirement_url="https://github.com/user/flask-app/blob/main/requirements.txt",
    update_at_startup=True,
    silent_mode=True,
    sleep_time=600  # Check every 10 minutes
)

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'loader_active': loader.auto_reload,
        'last_update': 'recent' if loader.first_update_made else 'none'
    })

@app.route('/force-update')
def force_update():
    try:
        # This will fail if auto_reload is True
        # You'd need to create a new loader instance or handle this differently
        self.loader.update(reload=True)
        return jsonify({'status': 'update triggered'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

### Example 2: Background Service

```python
# service.py
import time
import logging
from requirement_loader import RequirementLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundService:
    def __init__(self):
        self.loader = RequirementLoader(
            requirement_url="https://github.com/user/service/blob/main/requirements.txt",
            update_at_startup=True,
            auto_reload=True,
            sleep_time=900  # 15 minutes
        )
        
    def run_service(self):
        logger.info("Starting background service...")
        
        while True:
            try:
                # Your service logic here
                logger.info("Processing tasks...")
                self.process_tasks()
                
                time.sleep(30)  # Process every 30 seconds
                
            except KeyboardInterrupt:
                logger.info("Service interrupted")
                break
            except Exception as e:
                logger.error(f"Service error: {e}")
                time.sleep(5)  # Brief pause before retry
    
    def process_tasks(self):
        # Your actual service logic
        pass

if __name__ == '__main__':
    service = BackgroundService()
    service.run_service()
```

### Example 3: Microservice with Health Checks

```python
# microservice.py
from requirement_loader import RequirementLoader
import json
import time
from datetime import datetime

class MicroService:
    def __init__(self):
        self.start_time = datetime.now()
        self.update_count = 0
        
        # Custom loader with callbacks
        self.loader = RequirementLoader(
            requirement_url="https://github.com/company/microservice/blob/main/requirements.txt",
            update_at_startup=True,
            auto_reload=True,
            sleep_time=120  # 2 minutes
        )
        
        # Override the update method to add logging
        original_update = self.loader.update
        def logged_update(*args, **kwargs):
            self.update_count += 1
            print(f"Update #{self.update_count} at {datetime.now()}")
            return original_update(*args, **kwargs)
        
        self.loader.update = logged_update
    
    def get_status(self):
        return {
            'service': 'microservice',
            'status': 'running',
            'uptime': str(datetime.now() - self.start_time),
            'updates_performed': self.update_count,
            'loader_config': {
                'url': self.loader.requirement_url,
                'auto_reload': self.loader.auto_reload,
                'sleep_time': self.loader.sleep_time
            }
        }
    
    def run(self):
        print("Microservice starting...")
        print(json.dumps(self.get_status(), indent=2))
        
        try:
            while True:
                # Service logic here
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("Microservice shutting down...")

if __name__ == '__main__':
    service = MicroService()
    service.run()
```

## 🔧 Debugging and Troubleshooting

### Enable Verbose Logging

```python
import logging
from requirement_loader import RequirementLoader

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Disable silent mode to see pip output
loader = RequirementLoader(
    requirement_url="https://github.com/user/repo/blob/main/requirements.txt",
    silent_mode=False  # This will show pip installation output
)
```

### Testing URL Accessibility

```python
import requests
from requirement_loader import RequirementLoader

def test_url_accessibility(url):
    try:
        loader = RequirementLoader(auto_reload=False, update_at_startup=False)
        processed_url = loader._convert_to_raw_url(url)
        
        response = requests.get(processed_url)
        response.raise_for_status()
        
        print(f"✅ URL accessible: {processed_url}")
        print(f"📝 Content preview:\n{response.text[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ URL not accessible: {e}")
        return False

# Test your URL
test_url_accessibility("https://github.com/user/repo/blob/main/requirements.txt")
```

This comprehensive usage guide should help you implement Requirement Loader effectively in your projects. Remember to always test in a development environment before deploying to production!
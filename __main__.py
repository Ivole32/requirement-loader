import subprocess
import requests
import sys

def load_requirements(github_url: str):
    response = requests.get(github_url)
    content = response.text

    with open("requirements.txt", "w") as requirements:
        requirements.write(content)

def install_requirements():
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ], check=True)

def main():
    load_requirements("https://raw.githubusercontent.com/Ivole32/Status-Monitor/refs/heads/main/requirements.txt")
    install_requirements()

if __name__ == "__main__":
    main()
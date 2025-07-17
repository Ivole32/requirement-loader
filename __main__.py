import subprocess
import requests
import sys

def convert_to_raw_url(github_url: str) -> str:
    if "raw.githubusercontent.com" in github_url:
        return github_url
    
    if "github.com" in github_url and "/blob/" in github_url:
        return github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    
    return github_url

def load_requirements(url: str) -> None:
    if url.startswith("file://"):
        file_path = url[7:]
        with open(file_path, "r") as source_file:
            content = source_file.read()
    elif url.startswith(("http://", "https://")):
        url = convert_to_raw_url(url)
        response = requests.get(url)
        content = response.text

    with open("requirements.txt", "w") as requirements:
        requirements.write(content)

def install_requirements() -> None:
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ], check=True)

def main() -> None:
    load_requirements("https://github.com/Ivole32/gambling-simulator/blob/main/requirements.txt")
    #load_requirements("file:///home/ivo/GitHub/requirement-loader/requirements.txt")
    install_requirements()

if __name__ == "__main__":
    main()
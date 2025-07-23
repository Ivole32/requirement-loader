import subprocess
import threading
import requests
import time
import sys
import os

class RequirementLoader():
    def __init__(self, silent_mode: bool = True, sleep_time: int = 5) -> None:
        self.silent_mode = silent_mode
        self.sleep_time = sleep_time

        program = threading.Thread(target=self.start, kwargs={'silent_mode': self.silent_mode,
                                                              'sleep_time': self.sleep_time})
        program.daemon = True
        program.start()

        """while program.is_alive():
            time.sleep(1)

        exit(0)"""

    def start(self, silent_mode: bool = True, sleep_time: int = 5) -> None:
        while True:
            try:
                self.load_requirements("file:///home/ivo/GitHub/requirement-loader/testing/requirements.txt")
                self.install_requirements(silent_mode)
            except Exception as e:
                print(f"{e}")
            finally:
                time.sleep(sleep_time)

    def convert_to_raw_url(self, github_url: str) -> str:
        if "raw.githubusercontent.com" in github_url:
            return github_url
        
        if "github.com" in github_url and "/blob/" in github_url:
            return github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        
        return github_url

    def load_requirements(self, url: str) -> None:
        if url.startswith("file://"):
            file_path = url[7:]
            with open(file_path, "r") as source_file:
                content = source_file.read()
        elif url.startswith(("http://", "https://")):
            url = self.convert_to_raw_url(url)
            response = requests.get(url)
            content = response.text

        try:
            with open("requirements.txt", "r") as requirements:
                old_requirements = requirements.read()
        except:
            old_requirements = ""

        if old_requirements != content:
            with open("requirements.txt", "w") as requirements:
                requirements.write(content + "New Version")

    def install_requirements(self, silent: bool = True) -> None:
        with open("requirements.txt", "r") as requirements:
            requirements_content = requirements.read()

        with open("requirements.txt", "w") as requirements:
            new_version = False
            if "New Version" in requirements_content:
                requirements.write(requirements_content.replace("New Version", ""))
                new_version = True

        if silent:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        elif not silent and new_version:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], check=True)

    def reload_program(self) -> None:     
        main_file_path = os.path.abspath(sys.argv[0])
        python_exec = sys.executable
        args = sys.argv
        args.pop(0)
        command = python_exec + " " + main_file_path + " " + " ".join(f'"{arg}"' for arg in args)
        print(python_exec + str([main_file_path]) + str(args[1:]))
        os.execv(python_exec, [main_file_path] + args[1:])

if __name__ == "__main__":
    def main() -> None:
        loader = RequirementLoader(silent_mode=False)
        
    main() 
import subprocess
import threading
import requests
import inspect
import time
import sys
import os

class RestrictedArgumentError(Exception):
    pass

class ArgumentConflict(Exception):
    pass

class RequirementLoader():
    def __init__(self, requirement_url: str = "requirements.txt", update_at_startup: bool = True, silent_mode: bool = True, sleep_time: int = 5, auto_reload: bool = True) -> None:
        self.silent_mode = silent_mode
        self.sleep_time = sleep_time
        self.auto_reload = auto_reload
        self.update_at_startup = update_at_startup
        self.first_update_made = False
        self.new_version = False
        self.requirement_url = requirement_url

        if update_at_startup:
            self.update(reload=True, manual_update=False)

        if self.auto_reload:
            self.start_update_thread()

    def update(self, reload: bool = False, manual_update: bool = True) -> None:
        args = sys.argv
        caller_file = os.path.basename(inspect.stack()[1].filename)
        
        if manual_update == True and self.auto_reload == True:
            raise ArgumentConflict("You can't update manually when 'auto_reload' is enabled, disable it when the instance is created...")

        if manual_update == False and caller_file != "requirement_loader.py":
            raise RestrictedArgumentError("Argument 'manual_update' is internal and can only be set to 'False' by the class itself.")

        try:
            forced_update = True
            if "reloaded=True" in args:
                forced_update = False

            if manual_update:
                forced_update = True
                self.first_update_made = True

            self.load_requirements(self.requirement_url, force_update=forced_update)
            self.install_requirements(silent=self.silent_mode, reload=reload, forced_update=forced_update)
        except Exception as e:
            print(f"{e}")

    def start_update_thread(self) -> None:
        program = threading.Thread(target=self.update_thread, kwargs={'silent_mode': self.silent_mode,
                                                                    'sleep_time': self.sleep_time})
        program.daemon = True
        program.start()

    def update_thread(self, silent_mode: bool = True, sleep_time: int = 5) -> None:
        while True:
            try:
                self.load_requirements(self.requirement_url)
                self.install_requirements(silent_mode)
            except Exception as e:
                print(f"{e}")
            finally:
                time.sleep(sleep_time)

    def _convert_to_raw_url(self, url: str) -> str:
        if "raw.githubusercontent.com" in url:
            return url
        
        if "github.com" in url and "/blob/" in url:
            return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        
        return url

    def load_requirements(self, url: str, force_update: bool = False) -> None:
        if url.startswith("file://"):
            file_path = url[7:]
            with open(file_path, "r") as source_file:
                content = source_file.read()
        elif url.startswith(("http://", "https://")):
            url = self._convert_to_raw_url(url)
            response = requests.get(url)
            content = response.text

        try:
            with open("requirements.txt", "r") as requirements:
                old_requirements = requirements.read()
        except:
            old_requirements = ""

        if old_requirements != content or force_update:
            with open("requirements.txt", "w") as requirements:
                requirements.write(content)
            self.new_version = True
        else:
            self.new_version = False

    def install_requirements(self, silent: bool = True, forced_update: bool = False, reload: bool = None) -> None:
        if self.new_version or forced_update:
            if silent:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            elif not silent:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
                ], check=True)

            print(f"pip returncode: {str(result.returncode)}")
            if reload == None:
                print(f"reload=True")
            else:
                print(f"reload={str(reload)}")
            self.first_update_made = True

            if self.auto_reload or not (reload != None and reload == False):
                self._reload_program(reloaded=forced_update)

    def _reload_program(self, reloaded: bool = True) -> None:     
        main_file_path = os.path.abspath(sys.argv[0])
        python_exec = sys.executable

        print("[*] reloading")
        os.execv(python_exec, [python_exec, main_file_path] + sys.argv[1:] + [str(f"reloaded={str(reloaded)}")])

if __name__ == "__main__":
    def main() -> None:
        loader = RequirementLoader(silent_mode=False)
        
    main()
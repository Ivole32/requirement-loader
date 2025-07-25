from requirement_loader import RequirementLoader
from importlib.metadata import version
import time

requirement_url = "file:///home/ivo/GitHub/requirement-loader/testing/requirements.txt"
loader = RequirementLoader(requirement_url=requirement_url, update_at_startup=True, sleep_time=3, silent_mode=False, auto_reload=False)

i = 0
while True:
    i += 1
    print("Test")
    
    print(version("flask"))

    if i == 4:
        loader.update(reload=False)

    time.sleep(3)
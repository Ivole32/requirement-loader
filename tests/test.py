from requirement_loader import RequirementLoader
from importlib.metadata import version
import time

requirement_url = r"file://C:\Users\ivoth\Documents\GitHub\requirement-loader\testing\requirements.txt"
loader = RequirementLoader(requirement_url=requirement_url, update_at_startup=True, sleep_time=3, silent_mode=False, auto_reload=True)

i = 0
while True:
    try:
        i += 1
        print("Test")
        
        print(version("fastapi"))

        if i == 4:
            loader.update(reload=False)
            i = 0 # forgot that...

        time.sleep(3)
    except KeyboardInterrupt:
        break

exit(0)
from requirement_loader import RequirementLoader
import time

loader = RequirementLoader()

while True:
    print("Test")
    time.sleep(3)
    
    # Not working yet
    loader.reload_program()
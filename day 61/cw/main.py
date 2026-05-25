def jump():
    print("jump")

RUN_COUNT=1

def run():
    global RUN_COUNT
    print("run")
    RUN_COUNT += 1

def dash():
    print("dash")

def double_jump():
    print("double_jump")

def main():
    print("main")
    run()
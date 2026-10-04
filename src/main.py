import os
import shlex
import sys

VFS_name = "my_vfs"

def expand_env_variables(text):
    return os.path.expandvars(text)

def parse_input(raw_input):
    expanded = expand_env_variables(raw_input)
    return shlex.split(expanded)

def execute_command(tokens):
    if not tokens:
        return "", False
    cmd = tokens[0]
    args = tokens[1:]
    if cmd == "exit":
        if args:
            return "exit: too many arguments", False
        return "", True
    if cmd == "ls":
        return f"ls called with arguments: {args}", False
    if cmd == "cd":
        if len(args) > 1:
            return "cd: too many arguments", False
        return f"cd called with arguments: {args}", False
    return f"shell: command not found: {cmd}", False

def repl_loop():
    while True:
        try:
            raw_cmd = input(f"[{VFS_name}]$ ")
            if not raw_cmd.strip():
                continue
            tokens = parse_input(raw_cmd)
            msg, should_exit = execute_command(tokens)
            if should_exit:
                break
            if msg:
                print(msg)
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except ValueError as err:
            print(f"parse error: {err}")

if __name__ == "__main__":
    repl_loop()
    sys.exit(0)
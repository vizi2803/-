import os
import shlex
import sys
import argparse

DEFAULT_VFS_NAME = "my_vfs"

def expand_env_variables(text):
    return os.path.expandvars(text)

def parse_input(raw_input):
    expanded = expand_env_variables(raw_input)
    expanded = expanded.replace('\\', '/')
    tokens = shlex.split(expanded)
    return [token.replace('/', '\\') for token in tokens]

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

def process_command_line(line, VFS_NAME):
    clean_line = line.strip()
    if not clean_line:
        return False
    print(f"[{VFS_NAME}]$ {clean_line}")
    try:
        tokens = parse_input(clean_line)
    except ValueError as err:
        print(f"parse error: {err}")
        return False
    msg, should_exit = execute_command(tokens)
    if msg:
        print(msg)
        return should_exit

def run_startup_script(script_path, VFS_NAME):
    if not os.path.exists(script_path):
        print(f"error: startup script not found: {script_path}")
        return
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                should_exit = process_command_line(line, VFS_NAME)
                if should_exit:
                    break
    except OSError as err:
        print(f"error reading startup script: {err}")

def repl_loop(VFS_NAME):
    while True:
        try:
            raw_cmd = input(f"[{VFS_NAME}]$ ")
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

def parse_cli_args():
    parser = argparse.ArgumentParser(description="OS Shell Stage 2")
    parser.add_argument("--vfs", help="Path yo VFS phisical location")
    parser.add_argument("--script", help="Path yo startup script")
    return parser.parse_args()

def main():
    args = parse_cli_args()
    print("[DEBUG] Initialized shell configurayion:")
    print(f"  vfs_path: {args.vfs}")
    print(f"  startup_script: {args.script}")
    VFS_NAME = os.path.basename(args.vfs) if args.vfs else DEFAULT_VFS_NAME
    if args.script:
        run_startup_script(args.script, VFS_NAME)
    else:
        repl_loop(VFS_NAME)

if __name__ == "__main__":
    main()
    sys.exit(0)
#!/usr/bin/env python
import argparse
import sys
import os
import datetime
import time
import subprocess

DIARY_DIR = os.path.expanduser("~/.diary/")
EDITOR = "vim"

def get_args():
    parser = argparse.ArgumentParser(description="Command line diary")
    parser.add_argument("-l", "--list", action="store_true", help="List entries")
    return parser.parse_args(sys.argv[1:])

def get_config():
    return

def default_entry_name():
    return str(datetime.date.fromtimestamp(int(time.time())))

def edit_entry(entry_name = default_entry_name()):
    entry_path = os.path.join(DIARY_DIR, entry_name)
    subprocess.call([EDITOR, entry_path])

def main():
    args = get_args()

    if not os.path.isdir(DIARY_DIR):
        os.mkdir(DIARY_DIR)

    if args.list:
        return
    else:
        edit_entry()

if __name__ == "__main__":
    main()

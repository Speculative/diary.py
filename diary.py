#!/usr/bin/env python
import argparse
import ConfigParser
import sys
import os
import datetime
import time
import subprocess

DIARY_DIR = os.path.expanduser("~/.diary/")
CONFIG_FILE = ".diary.conf"
CONFIG = None
DEFAULT_CONFIG = {
    "editor": "vim"
}

def get_args():
    parser = argparse.ArgumentParser(description="Command line diary")
    parser.add_argument("-l", "--list", action="store_true", help="List entries")
    return parser.parse_args(sys.argv[1:])

def get_config():
    parser = ConfigParser.SafeConfigParser()
    config_path = os.path.join(DIARY_DIR, CONFIG_FILE)
    if os.path.isfile(config_path):
        parser.read(config_path)
        return parser._sections["Diary"]
    else:
        return None

def default_entry_name():
    return str(datetime.date.fromtimestamp(int(time.time())))

def edit_entry(entry_name = default_entry_name()):
    global CONFIG
    print type(CONFIG)
    print CONFIG
    entry_path = os.path.join(DIARY_DIR, entry_name)
    if ("editor" in CONFIG):
        subprocess.call([CONFIG["editor"], entry_path])
    else:
        subprocess.call([DEFAULT_CONFIG["editor"], entry_path])

def main():
    global CONFIG

    args = get_args()
    CONFIG = get_config()

    if not os.path.isdir(DIARY_DIR):
        os.mkdir(DIARY_DIR)

    if args.list:
        return
    else:
        edit_entry()

if __name__ == "__main__":
    main()

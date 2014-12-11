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
    parser.add_argument("-e", "--edit", action="store", nargs="?",
        const=default_entry_name(), help="--edit [entry]")
    parser.add_argument("-v", "--view", action="store", nargs="?",
        const=default_entry_name(), help="--view [entry]")
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

    entry_path = os.path.join(DIARY_DIR, entry_name)
    if ("editor" in CONFIG):
        subprocess.call([CONFIG["editor"], entry_path])
    else:
        subprocess.call([DEFAULT_CONFIG["editor"], entry_path])

def list_entries():
    entries = [entry for entry in os.listdir(DIARY_DIR)
        if os.path.isfile(os.path.join(DIARY_DIR, entry))
        and entry != CONFIG_FILE]
    for entry in entries:
        print entry

def view_entry(entry_name = default_entry_name()):
    entry_path = os.path.join(DIARY_DIR, entry_name)
    with open(entry_path) as f:
        line = f.readline()
        while line:
            print line
            line = f.readline()

def main():
    global CONFIG

    args = get_args()
    CONFIG = get_config()

    if not os.path.isdir(DIARY_DIR):
        os.mkdir(DIARY_DIR)

    if args.list:
        list_entries()
    elif args.view:
        view_entry(args.view)
    elif args.edit:
        edit_entry(args.edit)
    else:
        edit_entry()

if __name__ == "__main__":
    main()

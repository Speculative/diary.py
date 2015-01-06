#!/usr/bin/env python
import argparse
import ConfigParser
import sys
import os
import datetime
import time
import subprocess
import re

DIARY_DIR = os.path.expanduser("~/.diary/")
CONFIG_FILE = ".diary.conf"
CONFIG = None
DEFAULT_CONFIG = {
    "editor": "vim"
}

MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY",
    "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]

def get_args():
    parser = argparse.ArgumentParser(description="Command line diary")
    parser.add_argument("-l", "--list", action="store_true", help="List entries")
    parser.add_argument("-e", "--edit", action="store", nargs="+",
        help="--edit [entry]")
    parser.add_argument("-v", "--view", action="store", nargs="+",
        help="--view [entry]")
    parser.add_argument("-b", "--backup", action="store_true", help="Run backup")
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
    return str(datetime.datetime.now().date())

def edit_entry(entry_name = default_entry_name()):
    global CONFIG

    entry_name = parse_entry_name(entry_name)
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
    entry_name = parse_entry_name(entry_name)
    entry_path = os.path.join(DIARY_DIR, entry_name)

    if not os.path.isfile(entry_path):
        print "No entry for " + entry_name
        return

    with open(entry_path) as f:
        line = f.readline()
        while line:
            print line.rstrip()
            line = f.readline()

def parse_entry_name(entry_name):
    # Assumes something of the form January 1 2015
    # or 2015-01-01.
    global MONTHS
    global CONFIG

    SPECIAL_ENTRY_NAMES = ["TODAY", "YESTERDAY", "TOMORROW"]

    if isinstance(entry_name, list):
        entry_name = " ".join(entry_name)

    if re.match(r"\d{4}-\d{2}-\d{2}", entry_name):
        return entry_name
    elif entry_name.upper() in SPECIAL_ENTRY_NAMES:
        if entry_name.upper() == "TODAY":
            return default_entry_name()
        elif entry_name.upper() == "YESTERDAY":
            return str(datetime.datetime.now().date() -
                datetime.timedelta(days=1))
        elif entry_name.upper() == "TOMORROW":
            return str(datetime.datetime.now().date() +
                datetime.timedelta(days=1))
    else:
        if entry_name.count(" ") == 1:
            year = datetime.date.today().year
            month, day = entry_name.split(" ")
            month = month.upper()
            month = MONTHS.index(month) + 1
            return "%04d-%02d-%02d" % (year, month, int(day))
        elif entry_name.count(" ") == 2:
            month, day, year = entry_name.split(" ")
            month = month.upper()
            month = MONTHS.index(month) + 1
            return "%04d-%02d-%02d" % (year, month, int(day))
        else:
            print "Unrecognized date format!"

def backup():
    print "You tried to run a backup!"

def main():
    global CONFIG

    args = get_args()
    CONFIG = get_config()

    if not os.path.isdir(DIARY_DIR):
        os.mkdir(DIARY_DIR)

    if args.list:
        list_entries()
    elif args.backup:
        backup()
    elif args.view:
        view_entry(args.view)
    elif args.edit:
        edit_entry(args.edit)
    else:
        edit_entry()

if __name__ == "__main__":
    main()

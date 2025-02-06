# Git is CLI application, argparse is used to parse command line arguments
import argparse
# Git uses file format that is essentially INI format, so we use configparser
import configparser
# Git uses datetime for timestamps
from datetime import datetime
# For one use, read users and groups on Unix systems. Git saves the owners/group ID of files.
import grp, pwd
# fnmatch is used to match file names with patterns, we'll want it for .gitignore
from fnmatch import fnmatch
# Git uses SHA-1 function extensively, so we'll use hashlib
import hashlib
# Git uses math.ceil, so we'll import it
from math import ceil
# os and os.path are used to interact with the filesystem
import os
# re is used for regular expressions
import re
# sys to access command line arguments
import sys
# zlib is used for compression
import zlib

# Titling my application
argparser = argparse.ArgumentParser(description="Joe's stupiderist content tracker")

# Ensuring that the user has to provide a command
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

# Matching command line arguments to functions
def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Absolutely not. Not a command.")

# Example workflow. If wyag init --bare repo is called, argparse recognizes init as the subcommand
# Parses --bare and repo as arguments for init. args.command becomes init and the match statement
# executes the cmd_init(args) function. If defined, cmd_init(args) processes args.bare and args.directory

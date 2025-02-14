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

# Create repo object
class GitRepo (object):
    """A git repository"""
    # a repo has two components, a worktree for files in version control. Regular directory.
    workTree = None
    # and a git directory, where Git stores it's own data. Child directory of worktree, called .git
    gitDir = None
    conf = None

    def __init__(self, path, force=False):
        # assigning path to workTree
        self.workTree = path
        # creating gitDir with .git extension
        self.gitDir = os.path.join(path, ".git")

        # check if repo exists and contains subdirectory .git
        if not (force or os.path.isdir(self.gitDir)):
            raise Exception(f"Path: {path} is not a Git Repo")

        # read config file in .git/config
        self.conf = configparser.ConfigParser()
        # assign confif from repo file
        cf = repo_file(self, "config")

        # read config if exists and path exists
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        # check if not forced and raise error RE missing config
        elif not force:
            raise Exception("Config file missing")

        # if cf and cf path exist, then check if not force
        if not force:
            #get repo format version
            vers = int(self.conf.get("core", "repositoryformatversion"))
            # if not 0 raise exception
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion: {vers}")

# path building function. Variadic arg passed, allows for multiple path components.
def repo_path(repo, *path):
    """Create path under repo's git directory"""
    return os.path.join(repo.gitdir, *path)

# return and/or create path to file
def repo_file(repo, *path, mkdir=False):
    """create directory name if absent"""
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)

# return and/or create path to dir
def repo_path(repo, *path, mkdir=False):
    """same as repo_path but mkdir *path if absent & if mkdir"""
    path = repo_path(repo, *path)

    if os.path.exists(path):
        if (os.path.isdir(path)):
            return path
        else:
            raise Exception(f"{path} is NOT a directory")

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None

# to build new repo, start with dir and create .git dir inside.
def repo_create(path):
    """Create new repo in path"""
    repo = GitRepo(path, True)

    # first check path doesn't exist or is empty dir
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.workTree):
            raise Exception (f"{path} is not a directory")
        if os.path.exists(repo.gitDir):
            raise Exception (f"{path} is not empty")
    else:
        os.makedirs(repo.workTree)

    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo, "objects", mkdir=True)
    assert repo_dir(repo, "refs", "tags", mkdir=True)
    assert repo_dir(repo, "refs", "heads", mkdir=True)

    # .git/description
    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repo; edit this file 'description' to name the repo.\n")

    # .git/HEAD
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    # .git/config
    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo

# setting default config settings
def repo_default_config():
    """Set default config settings"""
    ret = configparser.ConfigParser()

    ret.add_section("core")
    # version of gitdir format. 0 is initial format, 1 same with extensions, >1 git will panic
    ret.set("core", "repositoryformatversion", "0")
    # disabling tracking of file models (permissions) changes in the work tree
    ret.set("core", "filemode", "false")
    # indicates this repo has worktree. Git supports optional worktree key that indicates location of worktree if not ".."
    ret.set("core", "bare", "false")

    return ret

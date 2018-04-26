# Created by Chuilian Kong Apr 25, 2018
# this script create a customized project boiler plate and sync it with github
# IMPORTANT: you must create a EMPTY project with specified name on github BEFORE running this script

import argparse
from pathlib import Path
import sys, datetime, os

# template library path
LIB_PATH = Path.cwd() / 'templates'

def parse_args():
    parser = argparse.ArgumentParser(description='create a project boiler plate and sync with github, note: you must create a empty project with specified name on github before running this script.')
    parser.add_argument('name', help='name of the project')
    parser.add_argument('author', help='author of the project')
    parser.add_argument('path', help='the desired root path of your new project')
    parser.add_argument('lang', help='the programming language you will use in this project')
    parser.add_argument('license', help='license of your project')

    return parser.parse_args()

# check if provided lang and license are supported
def args_check(args):
    if args.lang not in ['cc']:
        sys.exit('the provided lang is not supported.')

    if args.license not in ['MIT']:
        sys.exit('the provided license is not supported.')

# perform existance check and make a path obj
def make_path_obj(args):
    p = Path(args.path)
    if not p.exists() or not p.is_dir():
        sys.exit('the project root path is invalid.')

    p = p / args.name
    if p.exists():
        sys.exit('the project already exits at the given path.')

    return p

def make_dirs(p_root):
    p_root.mkdir()
    (p_root / 'src').mkdir()
    (p_root / 'test').mkdir()
    (p_root / 'build').mkdir()

def init_files(p_root, args):
    init_readme(p_root, args)
    init_license(p_root, args)

    if args.lang == 'cc':
        pass
    else:
        sys.exit('unsupported programming language.')

def init_readme(p_root, args):
    template = ''
    with (LIB_PATH / 'readme' / 'standard').open(mode='r') as rf:
        template = rf.read()
    with (p_root / 'README.MD').open(mode='w') as wf:
        wf.write(template.format(project_name=args.name))

def init_license(p_root, args):
    template = ''
    with (LIB_PATH / 'license' / 'MIT').open(mode='r') as rf:
        template = rf.read()
    with (p_root / 'LICENSE').open(mode='w') as wf:
        wf.write(template.format(year=datetime.datetime.now().year, author=args.author))

def main():
    args = parse_args()
    args_check(args)
    p_root = make_path_obj(args)
    make_dirs(p_root)
    init_files(p_root, args)

if __name__ == "__main__":
    main()

# Created by Chuilian Kong Apr 25, 2018
# this script create a customized project boiler plate and sync it with github
# IMPORTANT: you must create a EMPTY project with specified name on github BEFORE running this script

import argparse
from pathlib import Path
import sys, datetime, os, subprocess

# template library path
LIB_PATH = Path.cwd() / 'templates'

def parse_args():
    parser = argparse.ArgumentParser(description='create a project boiler plate and sync with github, note: you must create a empty project with specified name on github before running this script.')
    parser.add_argument('name', help='name of the project')
    parser.add_argument('author', help='author of the project')
    parser.add_argument('path', help='the desired root path of your new project')
    parser.add_argument('lang', help='the programming language you will use in this project')
    parser.add_argument('license', help='license of your project')
    parser.add_argument('repo', help='github repo of this project')

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

def make_dirs(p_root, args):
    p_root.mkdir()
    (p_root / 'src').mkdir()
    (p_root / 'test').mkdir()
    (p_root / 'build').mkdir()

def init_files(p_root, args):
    init_readme(p_root, args)
    init_license(p_root, args)

    if args.lang == 'cc':
        init_hello_world(p_root, args)
        init_cmake(p_root, args)
        init_gitignore_cc(p_root, args)
    else:
        sys.exit('unsupported programming language.')

# sync this project with your github repo
def sync_project(p_root, args):
    subprocess.run(args=['git', 'init'], cwd=p_root)

    subprocess.run(args=['git', 'add', '.gitignore'], cwd=p_root)
    subprocess.run(args=['git', 'commit', '-m', 'update gitignore'], cwd=p_root)

    subprocess.run(args=['git', 'add', 'README.md'], cwd=p_root)
    subprocess.run(args=['git', 'commit', '-m', 'update README.md'], cwd=p_root)

    subprocess.run(args=['git', 'add', 'LICENSE'], cwd=p_root)
    subprocess.run(args=['git', 'commit', '-m', 'update LICENSE'], cwd=p_root)

    subprocess.run(args=['git', 'add', '--all'], cwd=p_root)
    subprocess.run(args=['git', 'commit', '-m', 'init project'], cwd=p_root)

    subprocess.run(args=['git', 'remote', 'add', 'origin', args.repo], cwd=p_root)
    subprocess.run(args=['git', 'push', '-u', 'origin', 'master'], cwd=p_root)

############ file creators ################
def init_readme(p_root, args):
    template = read_from(LIB_PATH / 'readme' / 'standard')
    write_to(p_root / 'README.md', template.format(project_name=args.name))

def init_license(p_root, args):
    template = read_from(LIB_PATH / 'license' / 'MIT')
    write_to(p_root / 'LICENSE', template.format(year=datetime.datetime.now().year, author=args.author))

def init_hello_world(p_root, args):
    template = read_from(LIB_PATH / 'cc' / 'hello_world.cc')
    write_to(p_root / 'test' / 'hello_world.cc', template)

def init_cmake(p_root, args):
    template = read_from(LIB_PATH / 'cc' / 'CMakeLists')
    write_to(p_root / 'CMakeLists.txt', template.format(project_name=args.name))

def init_gitignore_cc(p_root, args):
    template = read_from(LIB_PATH / 'cc' / 'gitignore')
    write_to(p_root / '.gitignore', template)

def read_from(path):
    with path.open(mode='r') as f:
        return f.read()

def write_to(path, data):
    with path.open(mode='w') as f:
        f.write(data)


def main():
    args = parse_args()
    args_check(args)
    p_root = make_path_obj(args)
    make_dirs(p_root, args)
    init_files(p_root, args)
    sync_project(p_root, args)

if __name__ == "__main__":
    main()

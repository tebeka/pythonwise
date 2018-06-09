#!/usr/bin/env python
"""Create a .pex from a Python script"""

from argparse import ArgumentParser, FileType
from os.path import abspath, basename, dirname, isfile, splitext
from shutil import copy
from subprocess import run
from tempfile import mkdtemp
from uuid import uuid4

setup_template = '''
from distutils.core import setup

setup(
    name='{name}',
    scripts=['{script}'],
)
'''


log = None  # logging, set in main


def gen_requirements(script_dir, requirements, tmp_dir):
    reqs_file = f'{tmp_dir}/requirements.txt'
    user_reqs = f'{script_dir}/requirements.txt'

    if not requirements and isfile(user_reqs):
        log(f'requirements: {user_reqs}')
        copy(user_reqs, tmp_dir)
        return

    if not requirements:
        log('no requirements')
        with open(reqs_file, 'w') as out:
            pass
        return

    if len(requirements) == 1 and isfile(requirements[0]):
        log(f'using requirements file: {requirements[0]}')
        copy(requirements[0], reqs_file)
        return

    log(f'generating requirements file for: {requirements}')
    with open(reqs_file, 'w') as out:
        for req in requirements:
            print(req.strip(), file=out)


def gen_setup(script_dir, tmp_dir):
    user_setup = f'{script_dir}/setup.py'
    if isfile(user_setup):
        log(f'using setup - {user_setup}')
        copy(user_setup, tmp_dir)
        return

    log('generating setup.py')
    with open(f'{tmp_dir}/setup.py', 'w') as out:
        # We use random name to avoid pip caching
        out.write(setup_template.format(name=uuid4().hex, script=base))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('script', help='path to script', type=FileType('r'))
    parser.add_argument(
        '--requirements', '-r', default=[], action='append',
        help='path to requirements file or package name')
    parser.add_argument(
        '--verbose', '-v', help='be more verbose', action='store_true',
        default=False)
    parser.add_argument(
        '--output', '-o', default=None,
        help='output file name (by default script.py -> script.pex)')

    args = parser.parse_args()

    log = print if args.verbose else lambda msg: None

    script = args.script.name
    log(f'script: {script}')
    script_dir = dirname(abspath(script))
    base = basename(script)
    mod_name, _ = splitext(base)

    tmp_dir = mkdtemp()
    log(f'temp directory: {tmp_dir}')
    copy(script, tmp_dir)

    gen_requirements(script_dir, args.requirements, tmp_dir)
    gen_setup(script_dir, tmp_dir)

    tmp_pex = f'{mod_name}.pex'
    cmd = [
        'pex', '.',
        '-r', 'requirements.txt',
        '-o', tmp_pex,
        '-f', tmp_dir,
        '-c', base,
    ]
    log(' '.join(cmd))
    out = run(cmd, cwd=tmp_dir)
    if out.returncode != 0:
        raise SystemExit(out.returncode)

    out = args.output if args.output else f'{script_dir}/{tmp_pex}'
    copy(f'{tmp_dir}/{tmp_pex}', out)
    log(f'{out} created')

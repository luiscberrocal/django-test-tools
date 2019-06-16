import re
import subprocess
import sys


def run_commands(cmd):
    result = subprocess.run(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    lines = result.stdout.decode('utf-8').split('\n')[:-1]
    error_lines = result.stderr.decode('utf-8').split('\n')[:-1]
    return lines, error_lines


def get_new_version(lines):
    regexp = re.compile(r'new_version=(\d+\.\d+\.\d+)')
    for line in lines:
        match = regexp.match(line)
        if match:
            return match.group(1)


def print_lines(title, lines):
    if len(lines) > 0:
        print(title)
        print('-' * 80)
        c = 1
        for line in lines:
            print('Line {}: {}'.format(c, line))
            c += 1
        print('-' * 80)


def check_for_switched_branch(line):
    regexp = re.compile(r"Switched\sto\sa\snew\sbranch\s'release/(\d+\.\d+\.\d+)'")
    match = regexp.match(line)
    if match:
        return match.group(1)


def process_command(cmd, error_code, verbose):
    assert isinstance(verbose, bool)
    stdout_title = 'OUTPUT: ' + ' '.join(cmd)
    stderr_title = 'ERROR: ' + ' '.join(cmd)
    lines = run_commands(cmd)

    if verbose:
        print_lines(stdout_title, lines[0])
        print_lines(stderr_title, lines[1])
    if len(lines[1]) > 0:
        current_release = check_for_switched_branch(lines[1][0])
        if current_release is None:
            sys.exit(error_code)
    return lines


if __name__ == '__main__':
    import argparse

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--action", required=True,
                    help="Action patch, mayor or minor")

    args = vars(ap.parse_args())
    action = args['action']

    verbose = True
    cmd = ['bumpversion', action, '--list', '--dry-run', '--allow-dirty']  # , '|', 'grep' 'new_version']
    lines = process_command(cmd, 23, verbose)

    new_version = get_new_version(lines[0])
    if new_version:
        print('Version: {}'.format(new_version))
        cmd = ['git-flow', 'release', 'start', new_version]
        lines = process_command(cmd, 24, verbose)

        cmd = ['bumpversion', action]
        lines = process_command(cmd, 25, verbose)

        cmd = ['git', 'add', '.']
        lines = process_command(cmd, 26, verbose)

        cmd = ['git', 'commit', '-m', 'Updating version to {}'.format(new_version)]
        lines = process_command(cmd, 27, verbose)
    else:
        sys.exit(100)

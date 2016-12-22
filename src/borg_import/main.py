import argparse
import logging
import shutil
import shlex
import subprocess
import sys
from pathlib import Path

from .rsnapshots import get_snapshots

log = logging.getLogger(__name__)


def borg_import(args, archive_name, path, timestamp=None):
    borg_cmdline = ['borg', 'create']
    if timestamp:
        borg_cmdline += '--timestamp', timestamp.isoformat()
    if args.create_options:
        borg_cmdline.append(args.create_options)

    repository = args.repository.resolve()
    location = '{}::{}'.format(repository, archive_name)
    borg_cmdline.append(location)
    borg_cmdline.append('.')

    log.debug('Borg command line: %r', borg_cmdline)
    log.debug('Borg working directory: %s', path)
    subprocess.check_call(borg_cmdline, cwd=str(path))


def list_borg_archives(args):
    borg_cmdline = ['borg', 'list', '--short']
    repository = args.repository.resolve()
    borg_cmdline.append(str(repository))
    return subprocess.check_output(borg_cmdline).decode().split('\n')


def import_rsnapshot(args):
    existing_archives = list_borg_archives(args)

    import_path = args.rsnapshot_root / 'borg-import-dir'
    import_journal = args.rsnapshot_root / 'borg-import-dir.snapshot'

    if import_path.exists():
        print('{} exists. Cannot continue.'.format(import_path))
        return 1

    for rsnapshot in get_snapshots(args.rsnapshot_root):
        timestamp = rsnapshot['timestamp'].replace(microsecond=0)
        snapshot_original_path = rsnapshot['path']
        name = rsnapshot['name']
        archive_name = args.prefix + name

        if args.backup_sets and rsnapshot['backup_set'] not in args.backup_sets:
            print('Skipping (backup set is not selected):', name)
            continue

        if archive_name in existing_archives:
            print('Skipping (already exists in repository):', name)
            continue

        print('Importing {} (timestamp {}) '.format(name, timestamp), end='')
        if archive_name != name:
            print('as', archive_name)
        else:
            print()
        log.debug('  Moving {} -> {}'.format(rsnapshot['path'], import_path))

        with import_journal.open('w') as fd:
            fd.write('Current snapshot: %s\n' % rsnapshot['name'])
            fd.write('Original path: %s\n' % snapshot_original_path)

        snapshot_original_path.rename(import_path)

        try:
            borg_import(args, archive_name, import_path, timestamp=timestamp)
        finally:
            log.debug('  Moving {} -> {}'.format(import_path, rsnapshot['path']))
            import_path.rename(snapshot_original_path)
            import_journal.unlink()


def main():
    if not shutil.which('borg'):
        print('Borg does not seem to be installed. Please install Borg first.')
        print('See instructions at https://borgbackup.readthedocs.io/en/stable/installation.html')
        return 1

    common_parser = argparse.ArgumentParser(add_help=False)
    common_group = common_parser.add_argument_group('Common options')

    common_group.add_argument("--create-options", "-o",
                              help="Additional borg create options "
                                   "(note: Use -o=\"--foo --bar\" syntax to avoid parser confusion).")
    common_group.add_argument("--prefix", help="Add prefix to imported archive names", default='')

    common_group.set_defaults(log_level=logging.WARNING)
    common_group.add_argument("--debug", action='store_const', dest='log_level', const=logging.DEBUG,
                              help='Display debug/trace messages.')

    parser = argparse.ArgumentParser(description='Import existing backups from other software to Borg')


    subparsers = parser.add_subparsers()

    rsnapshot = subparsers.add_parser('rsnapshot', help='import rsnapshot backups', parents=[common_parser])
    rsnapshot.add_argument("--backup-set", help="Only consider given backup set (can be given multiple times).",
                           action='append', dest='backup_sets')
    rsnapshot.add_argument('rsnapshot_root', metavar='RSNAPSHOT_ROOT',
                           help='Path to rsnapshot root directory', type=Path)
    # TODO: support the full wealth of borg possibilities
    rsnapshot.add_argument('repository', metavar='REPOSITORY', help='Borg repository', type=Path)
    rsnapshot.set_defaults(function=import_rsnapshot)

    args = parser.parse_args()
    logging.basicConfig(level=args.log_level, format='%(message)s')

    if 'function' not in args:
        return parser.print_help()
    return args.function(args)


def below_main():
    # We Don't Go To Ravenholm
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as cpe:
        print('Borg invocation failed with status {}'.format(cpe.returncode))
        print('Command line was:', *[shlex.quote(s) for s in cpe.cmd])
        sys.exit(cpe.returncode)


if __name__ == "__main__":
    below_main()

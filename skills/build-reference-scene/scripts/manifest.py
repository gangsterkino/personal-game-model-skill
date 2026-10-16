"""Initialize or check a resumable scene manifest. Never overwrite on init."""
import argparse
import json
from pathlib import Path


def check(data):
    if data.get('schema_version') != 1:
        raise ValueError('unsupported schema_version')
    assets = data.get('assets')
    if not isinstance(assets, list):
        raise ValueError('assets must be a list')
    seen = set()
    for asset in assets:
        aid = asset.get('id')
        if not isinstance(aid, str) or not aid or aid in seen:
            raise ValueError('missing or duplicate asset id')
        seen.add(aid)
        count = asset.get('count', 1)
        if type(count) is not int or count < 1:
            raise ValueError(f'{aid}: invalid count')
        if asset.get('status') not in {'planned', 'submitted', 'ready', 'imported', 'failed'}:
            raise ValueError(f'{aid}: invalid status')
        if asset['status'] == 'submitted' and not asset.get('job_id'):
            raise ValueError(f'{aid}: submitted requires job_id')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['init', 'check'])
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    if args.action == 'init':
        with args.path.open('x', encoding='utf-8') as stream:
            json.dump({'schema_version': 1, 'reference': None, 'units': 'meters', 'assets': []}, stream, indent=2)
    else:
        check(json.loads(args.path.read_text(encoding='utf-8')))
    print('OK')


if __name__ == '__main__':
    main()

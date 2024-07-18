import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse


def custom_version_compare(version1, version2):
    def normalize(v):
        return [x for x in v.split('.')]

    v1 = normalize(version1)
    v2 = normalize(version2)
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0


async def fetch_json(session, branch):
    async with session.get(f'https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}') as response:
        return await response.json()


def compare_packages(package1, package2):
    results = {
        'only_in_first': [],
        'only_in_second': [],
        'in_first_higher_version': []
    }
    dict1 = {pkg['name']: pkg for pkg in package1}
    dict2 = {pkg['name']: pkg for pkg in package2}

    for pkg_name, pkg in dict1.items():
        if pkg_name not in dict2:
            results['only_in_first'].append(pkg)

    for pkg_name, pkg in dict2.items():
        if pkg_name not in dict1:
            results['only_in_second'].append(pkg)

    for pkg_name, pkg2 in dict2.items():
        if pkg_name in dict1:
            pkg1 = dict1[pkg_name]
            if custom_version_compare(pkg2['version'], pkg1['version']) > 0:
                results['in_first_higher_version'].append(pkg2)

    return results


def process_item(item):
    return item['arch'], item


def get_arches(libs_list):
    arch_dict = defaultdict(list)
    with ThreadPoolExecutor() as executor:
        future_to_item = {executor.submit(process_item, item): item for item in libs_list}
        for future in as_completed(future_to_item):
            arch, item = future.result()
            arch_dict[arch].append(item)
    return arch_dict


def cli_utility():
    parser = argparse.ArgumentParser(description='Compare binary packages between branches.')
    parser.add_argument('branch1', type=str, help='First branch to compare (e.g., sisyphus)')
    parser.add_argument('branch2', type=str, help='Second branch to compare (e.g., p10)')

    args = parser.parse_args()
    return args.branch1, args.branch2


def set_json(dict1, dict2):
    result = {}
    futures = []
    with ThreadPoolExecutor() as executor:
        for arch in set(dict1.keys()) & set(dict2.keys()):
            futures.append(
                executor.submit(
                    compare_packages,
                    *[dict1.get(arch, []), dict2.get(arch, [])]
                )
            )
        for future in as_completed(futures):
            res = future.result()
            result['arch'] = {
                'only_in_first': res['only_in_first'],
                'only_in_second': res['only_in_second'],
                'in_first_higher_version': res['in_first_higher_version']
            }

    print(json.dumps(result, indent=4))


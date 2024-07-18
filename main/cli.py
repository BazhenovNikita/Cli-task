import aiohttp
import asyncio
from utils import cli_utility, fetch_json, get_arches, set_json


async def main():
    branches = cli_utility()

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            fetch_json(session, branches[0]),
            fetch_json(session, branches[1])
        )
    arches_dict1 = get_arches(results[0]['packages'])
    arches_dict2 = get_arches(results[1]['packages'])
    set_json(arches_dict1, arches_dict2)


if __name__ == '__main__':
    asyncio.run(main())

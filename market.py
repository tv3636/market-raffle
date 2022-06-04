import requests
import json
import time

API = 'https://api.reservoir.tools/sales/v3?contract=%s&limit=20'

contracts = [
	'0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42',
	'0x9690b63eb85467be5267a3603f770589ab12dc95',
	'0x251b5f14a825c537ff788604ea1b58e49b70726f',
	'0xf55b615b479482440135ebf1b907fd4c37ed9420',
	'0x31158181b4b91a423bfdc758fc3bf8735711f9c5',
	'0x8634c23d5794ed177e9ffd55b22fdb80a505ab7b',
	'0xda5cf3a42ebacd2d8fcb53830b1025e01d37832d',
	'0x7de11a2d9e9727fa5ead3094e40211c5e9cf5857'
]

eligible = {}

for contract in contracts:
	started = False
	continuation = None
	oldest = time.time()

	while (not started or continuation) and (oldest > 1652907600):
		url = API % contract

		if continuation:
			url += '&continuation=' + continuation

		response = requests.get(url).json()

		for sale in response['sales']:
			oldest = min(oldest, sale['timestamp'])

			if sale['orderSource'] == 'Forgotten Market':
				eligible[sale['from']] = 1
				eligible[sale['to']] = 1

		if 'continuation' in response:
			continuation = response['continuation']

		print(contract, oldest, continuation)

		started = True

print(list(eligible.keys()))
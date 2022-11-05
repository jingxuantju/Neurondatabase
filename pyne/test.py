from netpyne import specs
netParams = specs.NetParams()

# Method 1: direct
netParams.popParams['Pop1'] = {'cellType': 'PYR', 'numCells': 20}

# Method 2: using object method
netParams.addPopParams(label='Pop1', params={'cellType': 'PYR', 'numCells': 20})
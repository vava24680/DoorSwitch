import DAN

ServerURL = 'http://DomainName:9999'   #=None:AutoSearch, or ='IP':Connect to this IP
#ServerIP = 'https://DomainName'   #=None:AutoSearch, or ='IP':Connect to this IP
Comm_interval = 0.5 # unit:second

def profile_init():
    DAN.profile['dm_name'] = 'Door'
    DAN.profile['d_name'] = DAN.profile['dm_name'] + '.' + DAN.get_mac_addr()[-4:]

def odf():  # int only
    # Return a list of tuples
    # Each tuple consists of 3 elements,
    # first is the feature name
    # second is the index of this tuple in this list
    # third is the key name of one key-value pair that will be used in bridge
    return [
        ('Open', 0, 'Open')
    ]

def idf():
    return [
     #  ('PIN1', float),
     #  ('PIN2', int),
     #  ('PIN3', str),
    ]

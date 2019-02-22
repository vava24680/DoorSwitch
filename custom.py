import DAN

ServerIP = 'http://IP:9999'   #=None:AutoSearch, or ='IP':Connect to this IP
#ServerIP = 'https://DomainName'   #=None:AutoSearch, or ='IP':Connect to this IP
Comm_interval = 0.5 # unit:second

def profile_init():
    DAN.profile['dm_name']='Windows'
    DAN.profile['d_name']=DAN.profile['dm_name']+'.'+DAN.get_mac_addr()[-4:]

def odf():  # int only
    return [
        ('Switch', 0, 'Switch'),
    ]

def idf():
    return [
     #  ('PIN1', float),
     #  ('PIN2', int),
     #  ('PIN3', str),
    ]

import sys
import time
import DAN
import requests
import os

sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient
import custom

client = BridgeClient()

custom.profile_init()
odf_list = custom.odf()
idf_list = custom.idf()

DAN.profile['df_list'] = [t[0] for t in idf_list]

for t in odf_list:
    if t[0] not in DAN.profile['df_list']:
        DAN.profile['df_list'].append(t[0])

print('Detected features:')
for f_name in DAN.profile['df_list']:
    print('    {}'.format(f_name))


def LED_flash(LED_state):
    if LED_state:
        client.put('Reg_done', '1')
        os.system(r'echo "timer" > /sys/class/leds/ath9k-phy0/trigger')      #For ArduinoYun Only. LED Blink.
    else:
        client.put('Reg_done', '0')
        os.system(r'echo "none" > /sys/class/leds/ath9k-phy0/trigger')

DAN.device_registration_with_retry(custom.ServerURL)
LED_flash(1)

incomming = {}
for f_name in [t[0] for t in odf_list]:
    incomming[f_name] = 0

reConnecting = 0
while True:
    try:
        cache = {}
	check_list=[t[0] for t in odf_list]
	for f_name, index, pin_name in odf_list:

            if f_name not in cache.keys():
                os.system(r'echo "default-on" > /sys/class/leds/ath9k-phy0/trigger')
  	        PIN = DAN.pull(f_name)
		cache[f_name] = PIN
            else:
	        PIN = cache[f_name]

            if PIN != None:

                check_list.remove(f_name)

                if PIN[index] != None:
                    client.put(pin_name, str(int(PIN[index])))
                else:
                    continue

                if f_name not in check_list:
                    incomming[f_name] = (incomming[f_name] + 1) % 10000
                    #client.put('incomming_'+f_name, str(incomming[f_name]))
                    #print ('Bridge: change incomming state of '+f_name)

                print '{f}[{d}] -> {p} = {v}, incomming[{f}] = {i}'.format(
                        f=f_name,
                        d=index,
                        p=pin_name,
                        v=str(int(PIN[index])),
                        i=incomming[f_name],
                )
            os.system(r'echo "none" > /sys/class/leds/ath9k-phy0/trigger')


        for f_name, type_ in idf_list:
            tmp = client.get(f_name)
            if tmp is None:
                continue
            else:
                client.delete(f_name)

            v = type_(tmp)
            if v is not None:
                os.system(r'echo "default-on" > /sys/class/leds/ath9k-phy0/trigger')
                print 'DAN.push({f}, {v!r})'.format( f=f_name, v=v,)
                DAN.push(f_name, v)
                os.system(r'echo "none" > /sys/class/leds/ath9k-phy0/trigger')

        if reConnecting:
            LED_flash(1)
            reConnecting = 0

    #except KeyboardInterrupt:
    #    DAN.deregister()
    #    LED_flash(0)
    #    break

    except Exception, e:
        print(e)
        LED_flash(0)

        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            reConnection = 1
            DAN.device_registration_with_retry(custom.ServerURL)
        else:
            print('Connection failed due to unknow reasons.')
            reConnecting = 1
            time.sleep(1)

    time.sleep(custom.Comm_interval)

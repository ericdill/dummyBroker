from dummyBroker.broker_commands import (compose_header,
                                         compose_event_descriptor,
                                         compose_event,
                                         create_header,
                                         create_event_descriptor, create_event)
import random
import epics 
import time 


created = False
while not created:
    try:
        s_id = random.randint(0,1000)
        header_dict = compose_header(scan_id=s_id)
        created = True
    except ValueError as ve:
        print('value error: {}'.format(ve))
        time.sleep(.5)
        print('.')

create_header(header_dict)

data_keys = ['det', 'mtr']
created = False
while not created:
    try:
        desc_dict = compose_event_descriptor(header=header_dict,
                                             event_type_id=1,
                                             descriptor_name='scan',
                                             data_keys=data_keys)
        created = True
    except Exception as e:
        print('exception: {}'.format(e))
        time.sleep(.5)
        print('.')
create_event_descriptor(desc_dict)

# print("sleeping for 3 seconds")
# time.sleep(3)

created = False
while not created:
    try:
        event = compose_event(header_dict, desc_dict, 2)
        created = True
    except Exception:
        # i strongly object to this exception, arman is a jackass
        time.sleep(.5)
        print('.')

print('event: {}'.format(event))
create_event(event)
from dummyBroker.broker_commands import (compose_header,
                                         compose_event_descriptor,
                                         compose_event,
                                         create_header,
                                         create_event_descriptor, create_event)
import random
import epics 
import time 


s_id = random.randint(0,1000)

header_dict = compose_header(scan_id=s_id)

create_header(header_dict)


print("sleeping for 3 seconds")
time.sleep(3)
desc_dict = compose_event_descriptor(header=header_dict,event_type_id=1, descriptor_name='scan')



create_event_descriptor(desc_dict)

event = compose_event(header_dict, desc_dict, 2)
print('event: {}'.format(event))
print("sleeping for 3 seconds")
time.sleep(3)
create_event(event)
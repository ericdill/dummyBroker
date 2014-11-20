from broker_commands import compose_header, compose_event_descriptor
from broker_commands import create_header, create_event_descriptor, create_event
import random
import epics 
import time 


s_id = random.randint(0,1000)

header_dict = compose_header(scan_id=s_id)

create_header(header_dict)


time.sleep(1)
desc_dict = compose_event_descriptor(header=header_dict,event_type_id=1, descriptor_name='scan')



create_event_descriptor({'descriptor_name': 'scan', 'scan_id': 218, 'event_type_id': 1}) 


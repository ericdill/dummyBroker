import time
import json
import epics
from metadataStore.collectionapi.commands import create, record


header_PV = "XF:23ID-CT{Replay}Val:RunHdr-I"
event_PV = "XF:23ID-CT{Replay}Val:EventHdr-I"



def header_callback(value, **kw):
    raw_data = kw['char_value']
    print raw_data
    data = json.loads(raw_data)
    if data.has_key('header'):
        create(header=data['header'])
        print 'Created header entry'
    if data.has_key('event_descriptor'):
        print '                \n\n\n', data
        print '\n\n\n here is event descriptor i received', data['event_descriptor']
        create(event_descriptor=data['event_descriptor']) 
        print 'Created event_descriptor entry'    

def event_callback(value, **kw):
    raw_data = kw['char_value']
    data = json.loads(raw_data)
    record(event=data)
    print 'Created event entry'



hdr_pv = epics.PV(header_PV, auto_monitor=True)
hdr_pv.add_callback(header_callback)


#hdr_pv = epics.PV(event_PV, auto_monitor=True)
#hdr_pv.add_callback(event_callback)



print 'Now wait for changes'

t0 = time.time()
#while time.time()-t0 < 300:
while True:
    time.sleep(0.01)


print 'Broker stopped!'

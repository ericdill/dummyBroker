import time
import json
import epics
from metadataStore.collectionapi.commands import create, record


header_PV = "XF:23ID-CT{Replay}Val:RunHdr-I"
event_PV = "XF:23ID-CT{Replay}Val:EventHdr-I"



def header_callback(value, **kw):
    """
    Header and event descriptor should already be created by the data
    broker before they are published to the header PV, as this callback will
    not create PVs.

    :param value:
    :param kw:
    :return:
    """
    raw_data = kw['char_value']
    print raw_data
    data = json.loads(raw_data)
    try:
        header = data['header']
        print("=============="
              "\nHeader: {}"
              "==============".format(header))
    except KeyError as ke:
        print('No run header present')
    try:
        event_descriptors = data['event_descriptors']
        num_ev_desc = 1
        if (isinstance(event_descriptors, list)
            or isinstance(event_descriptors, tuple)):
            num_ev_desc = len(event_descriptors)
        else:
            num_ev_desc = 1
            event_descriptors = [event_descriptors, ]

        print("{} Event descriptors are present".format(num_ev_desc))
        for idx, ev_desc in enumerate(event_descriptors):
            print("==============\nEvent descriptor {}: {}\n=============="
                  "".format(idx, ev_desc))
    except KeyError as ke:
        print('No event descriptor present')


def event_callback(value, **kw):
    raw_data = kw['char_value']
    data = json.loads(raw_data)
    record(event=data)
    print 'Created event entry'



hdr_pv = epics.PV(header_PV, auto_monitor=True)
hdr_pv.add_callback(header_callback)


hdr_pv = epics.PV(event_PV, auto_monitor=True)
hdr_pv.add_callback(event_callback)



print 'Now wait for changes'

t0 = time.time()
#while time.time()-t0 < 300:
while True:
    time.sleep(0.01)


print 'Broker stopped!'

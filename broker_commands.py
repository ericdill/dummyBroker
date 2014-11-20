__author__ = 'arkilic'
import datetime
from metadataStore.collectionapi.commands import find as _find
from metadataStore.collectionapi.commands import create as _create
from metadataStore.collectionapi.commands import record as _record
import epics
import json


header_PV = "XF:23ID-CT{Replay}Val:RunHdr-I"
event_PV = "XF:23ID-CT{Replay}Val:EventHdr-I"

def compose_header(scan_id, **kwargs):
    """
    For valid keys in kwargs, see 'header_keys_dict'
    """
    header = dict()
    provided_keys = kwargs.keys()
    for key in provided_keys:
        if header_keys_dict.has_key(key):
            if isinstance(kwargs[key], header_keys_dict[key]['type']):
                pass
            else:
                raise TypeError('Given type is not valid for ', key, ' Should be ', header_keys_dict['type'])
        else:
            raise ValueError("The provided key is invalid for header", key)
    header = kwargs
    res = _find(scan_id = scan_id)
    if res:
        raise ValueError('A scan with this id exists ', scan_id)
    else:
        header['scan_id'] = scan_id
    return header


def create_header(header):
    packaged_header = dict()
    header_pv = epics.PV(header_PV)
    try:
        packaged_header['header'] = header
        #_create(header=header)
        dumped_hdr = json.dumps(packaged_header)
        print 'Writing to PV', dumped_hdr
        header_pv.put(dumped_hdr)
    except:
        raise

def create_event_descriptor(event_descriptor):
    header_pv = epics.PV(header_PV)
    packaged_desc = dict()
    print '\n\n\n here it is!!!!!!',type(event_descriptor['descriptor_name'])
    

    try:
        packaged_desc['event_descriptor'] = event_descriptor
        #_create(event_descriptor=event_descriptor)
        dumped_ev_desc = json.dumps(packaged_desc)
        print dumped_ev_desc
        header_pv.put(dumped_ev_desc)
    except:
        raise

def create_event(event):
    event_pv = epics.PV(event_PV)
    try:
        #_record(event=event)
        dumped_ev = json.dumps(event)
        event_pv.put(dumped_ev)
    except:
        raise

def compose_event_descriptor(header, event_type_id, descriptor_name, **kwargs):
    """
    For valid keys in kwargs, see 'event_descriptor_keys_dict'
    """
    event_descriptor = dict()
    provided_keys = kwargs.keys()
    for key in provided_keys:
        if event_desc_keys_dict.has_key(key):
            if isinstance(kwargs[key], event_desc_keys_dict[key]['type']):
                pass
            else:
                raise TypeError('Given type is not valid for ', key, ' Should be ', header_keys_dict['type'])
        else:
            raise ValueError("The provided key is invalid for header", key)
    event_descriptor = kwargs
    scan_id = header['scan_id']
    event_descriptor['descriptor_name'] = str(descriptor_name)
    res = _find(scan_id = scan_id)
    if res:
        pass
    else:
        raise Exception('Header with given scan_id is not yet created')
    event_descriptor["event_type_id"] = int(event_type_id)
    event_descriptor["scan_id"] = scan_id

    return event_descriptor

def compose_event(header, descriptor, seq_no, **kwargs):
    """
    For valid keys in kwargs, see 'event_keys_dict'
    """
    event = dict()
    provided_keys = kwargs.keys()
    for key in provided_keys:
        if event_keys_dict.has_key(key):
            if isinstance(kwargs[key], event_keys_dict[key]['type']):
                pass
            else:
                raise TypeError('Given type is not valid for ', key, ' Should be ', header_keys_dict['type'])
        else:
            raise ValueError("The provided key is invalid for header", key)
    event = kwargs
    event['seq_no'] = seq_no
    scan_id = header['scan_id']
    res = _find(scan_id = scan_id)
    if res:
        pass
    else:
        raise Exception('Header with given scan_id is not yet created')
    
    descriptor_name = descriptor["descriptor_name"]
    event = kwargs
    event["scan_id"] = scan_id
    event[descriptor_name] = descriptor_name
    return event

header_keys_dict = dict()
#TODO: Change to OrderedDict

header_keys_dict["scan_id"] = {"description": "The unique identifier of the run",
                               "type": int}

header_keys_dict["owner"] = { "description": "The user name of the person that created the header",
                              "type": str}

header_keys_dict["start_time"] = { "description": "The start time in utc",
                                   "type": datetime.datetime}

header_keys_dict["status"] = { "description": 'Run header completion status( In Progress/Complete',
                               "type": str}

header_keys_dict["beamline_id"] = { "description": "Beamline identifiying string",
                                    "type": str}

header_keys_dict["custom"] = { "description": " Additional attribute value fields that can be user defined",
                               "type": dict}

event_desc_keys_dict = dict()
event_desc_keys_dict['header'] = { "description": " Run header associated with an event descriptor",
                                   "type": dict}

event_desc_keys_dict['event_type_id'] = { "description": " Run header associated with an event descriptor",
                                          "type": int}

event_desc_keys_dict['type_descriptor'] = { "description": " Additional information regarding event_type_desc",
                                            "type": dict}


event_keys_dict = dict()

event_keys_dict['header'] = { "description": " Run header associated with an event descriptor",
                                   "type": dict}

event_keys_dict['event_descriptor'] = { "description": "Event descriptor asssociated with a specific event",
                                             "type": dict}

event_keys_dict['seq_no'] = { "description": "Sequence number for the event wrt other events",
                                   "type": int}

event_keys_dict['owner'] = { "description": "The user name of the person that created the header",
                             "type": str}

event_keys_dict['description'] = { "description": "String identifier describing nature of an event",
                                   "type": str}

event_keys_dict['data'] = { "description": "Data point name-value pair container",
    "type": dict}


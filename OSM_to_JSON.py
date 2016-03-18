# -*- coding: utf-8 -*-
"""
Created on Sat Aug 08 14:52:50 2015

@author: Ryan
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import codecs
import json


filename = 'C:/Users/Ryan/Desktop/Project_3_OSM/syracuse_new-york.osm'
mapping = {'Courts' : 'Court'}
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


# Pull and shape desired data from OSM file
def shape_element(element):
    node = {'created' : {}}
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        for x in element.attrib:
            if x == 'lat':
                try:
                    node['pos'][0] = float(element.attrib['lat'])
                except:
                    node['pos'] = [float(element.attrib['lat'])]
            elif x == 'lon':
                try:
                    node['pos'].append(float(element.attrib['lon']))
                except:
                    node['pos'] = [0, float(element.attrib['lon'])]
            elif x in CREATED:
                node['created'][x] = element.attrib[x]
            else:
                node[x] = element.attrib[x]
        # Check for K elements in Tags and append non-problem values to node dict
        for x in element:
            if 'k' in x.attrib and not problemchars.search(x.attrib['k']):
                if x.attrib['k'].split(':')[0] == 'addr' and len(x.attrib['k'].split(':'))>2:
                    pass
                elif x.attrib['k'].split(':')[0] == 'addr' and len(x.attrib['k'].split(':'))<3 and lower_colon.search(x.attrib['k']):
                    try:
                        node['address'][x.attrib['k'].split(':')[1]] = x.attrib['v']
                    except:
                        node['address'] = {x.attrib['k'].split(':')[1]: x.attrib['v']}
                else:
                    node[x.attrib['k']] = x.attrib['v']
            elif 'ref' in x.attrib:
                if 'node_refs' in node:
                    node['node_refs'].append(x.attrib['ref'])
                else:
                    node['node_refs'] = []
                    node['node_refs'].append(x.attrib['ref'])
        return node
    else:
        return None



def update_street(entry):
    # Modify street types and names to be consistant
    expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", 'Way', 'Terrace', 'Circle', 'Plaza', 'Center', 'North',
            'South','East','West']
    mapping = {'Courts' : 'Court', 'Route 11' : 'US Route 11'}
    street = ''
    if 'address' in entry:
        if 'street' in entry['address']:
            street = entry['address']['street']
            m = street_type_re.search(street).group()
            name = street.split(' ')
            if m in mapping.keys():
                name[-1] = mapping[name[-1]]
            name = ' '.join(name)
            if name in mapping:
                name = mapping[name]
            entry['address']['street'] = name
    return entry
    
def update_zip(entry):
    # Remove additional zip code information where more than 5 digits are present
    if 'address' in entry:
        if 'postcode' in entry['address'] and entry['address']['postcode'] == '14224':
            entry['address']['postcode'] = '13224'
        elif 'postcode' in entry['address'] and len(entry['address']['postcode']) > 5:
            entry['address']['postcode'] = entry['address']['postcode'][:5]
    return entry
        


def process_map(filename, file_out):
    # Write JSON file from selected OSM file data
    file_out = "C:/Users/Ryan/Desktop/Project_3_OSM/syracuse.json".format(filename)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(filename):
            el = shape_element(element)
            if el:
                el = update_street(el)
                el = update_zip(el)
                data.append(el)
                if file_out:
                    fo.write(json.dumps(el) + "\n")
                    
    return data

if __name__ == '__main__':
    process_map(filename, False)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
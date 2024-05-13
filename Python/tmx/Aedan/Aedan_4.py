import os
from lxml import etree
from datetime import datetime

def merge_tmx_files(directory):
    
    root = etree.Element('tmx')
    header = None
    body = etree.SubElement(root, 'body')

    existing_tus = set()
    tus_with_dates = []

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename=='project_save.tmx':
                tree = etree.parse(os.path.join(dirpath, filename))
                print(dirpath, filename)
                if header is None:
                    header = tree.find('header')
                    root.insert(0, header)
                for tu in tree.xpath('//tu'):
                    tu_string = etree.tostring(tu)
                    if tu_string not in existing_tus:
                        existing_tus.add(tu_string)
                        for tuv in tu.xpath('.//tuv'):
                            changedate = tuv.get('changedate')
                            if changedate:
                                changedate_datetime = datetime.strptime(changedate, "%Y%m%dT%H%M%SZ")
                                tus_with_dates.append((changedate_datetime, tu))


    tus_with_dates.sort(key=lambda x: x[0])


    for _, tu in tus_with_dates:
        body.append(tu)

    with open('project_save.tmx', 'wb') as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

merge_tmx_files('C:/Users/Рома/Dropbox/Archolos/OmegaT')

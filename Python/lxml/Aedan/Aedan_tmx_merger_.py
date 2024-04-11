import os
import sys
from lxml import etree

def merge_tmx_files(directory):
    
    root = etree.Element('tmx')
    header = None
    body = etree.SubElement(root, 'body')

    existing_tus = set()

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('project_save.tmx'):
                tree = etree.parse(os.path.join(dirpath, filename))
                if header is None:
                    header = tree.find('header')
                    root.insert(0, header)
                for tu in tree.xpath('//tu'):
                    tu_string = etree.tostring(tu)
                    if tu_string not in existing_tus:
                        existing_tus.add(tu_string)
                        body.append(tu)
                print(filename, ' appended')
    
    merged_tmx_path = os.path.join(directory_path, "project_save_MERGED.tmx")
    with open(merged_tmx_path, 'wb') as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Using: python script.py <folder_path>")
        sys.exit(1)
    else:
        directory_path = sys.argv[1]
        directory_path = os.path.normpath(directory_path)
        merge_tmx_files(directory_path)

# merge_tmx_files('D:/Dropbox/Archolos/OmegaT')

import xml.etree.ElementTree as ET
import random

#Function to remove an XML element if its tag or attribute matches the specified line
def remove_xml_line(content: str, line_to_remove: str):
    root = ET.fromstring(content)

    for elem in root.iter():
        if line_to_remove in str(elem.attrib) or line_to_remove in str(elem.tag):
            parent = elem.getparent()
            if parent is not None:
                parent.remove(elem)

    return ET.tostring(root, encoding="unicode")

#Function to obfuscate XML attributes or remove entire elements based on specified parameters
def obfuscate_xml(content: str, num_to_obfuscate: int = 1, obf_value: str | None = None, frac_to_obfuscate: float | None = None, remove_entire_line: bool = False):
    root = ET.fromstring(content)

    #Define XML namespaces and register the Android namespace if applicable
    namespaces = {"android": "http://schemas.android.com/apk/res/android"}
    android_ns = namespaces["android"]

    ET.register_namespace("android", android_ns)

    #Collect all XML attributes and establish parent-child relationships
    all_attributes = []
    parent_map = {child: parent for parent in root.iter() for child in parent}
    for element in root.iter():
        for attr_key in element.attrib:
            all_attributes.append((element, attr_key))

    #Determine the number of attributes to obfuscate based on fraction input
    if frac_to_obfuscate is not None:
        num_to_obfuscate = max(int(len(all_attributes) * frac_to_obfuscate), 1)
    num_to_obfuscate = min(num_to_obfuscate, len(all_attributes))

    #Randomly select attributes for obfuscation
    attributes_to_obfuscate = random.sample(all_attributes, num_to_obfuscate)
    obfuscated_lines = []

    for element, attr_key in attributes_to_obfuscate:
        if obf_value is None: #Determine if attribute should be removed or element deleted
            if remove_entire_line:
                parent = parent_map.get(element)
                if parent is not None and element in parent:
                    obfuscated_lines.append(ET.tostring(element, encoding="unicode"))
                    parent.remove(element)  #Remove the entire element from the XML tree
            else:
                del element.attrib[attr_key] #Remove only the attribute, preserving the element
        else:
            element.attrib[attr_key] = obf_value #Replace attribute value with the specified obfuscation value

    if remove_entire_line:
        return ET.tostring(root, encoding="unicode"), obfuscated_lines
    else:
        return ET.tostring(root, encoding="unicode"), attributes_to_obfuscate
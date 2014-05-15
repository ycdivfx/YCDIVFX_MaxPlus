import xml.etree.ElementTree as ET

import MaxPlus


def prettyxml(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            prettyxml(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def main():
    MaxPlus.Core.EvalMAXScript('clearListener()')

    if MaxPlus.Core.GetRootNode().GetNumChildren() == 0:
        print 'No objects in scene'
        return

    xmlroot = ET.Element('RootNode')
    document = ET.ElementTree(xmlroot)

    for obj in MaxPlus.Core.GetRootNode().Children:
        assert isinstance(obj, MaxPlus.INode)
        node = ET.SubElement(xmlroot,'Object')
        assert isinstance(node, ET.Element)
        node.set('Name', obj.Name)
        node.set('WireColor', str(obj.WireColor))

    prettyxml(xmlroot)

    print ET.tostring(xmlroot)
    document.write(r'C:\3dsmax.xml', encoding='utf-8', xml_declaration=True,)

if __name__ == '__main__':
    main()
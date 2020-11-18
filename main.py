import os
import pdb
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
from xml.etree.ElementTree import ElementTree, Element

def read_xml(annoPath):
    tree = ET.parse(annoPath)
    root = tree.getroot()
    xml_content = open(annoPath).read()
    return tree, root, xml_content
def test():
    imgRootPath = './test_voc/images/'
    annoRootPath = './test_voc/annotations/'
    # for file in os.listdir(annoRootPath):
    #     domTree = parse(annoRootPath + file)
    #     root = domTree.documentElement

    # 从xml文件中读取，使用getroot()获取根节点，得到的是一个Element对象
    # tree = ET.parse(annoRootPath + './100009.xml')
    # print('tree', type(tree))
    # root = tree.getroot()
    # print('root', type(root))

    tree, root, xml_content = read_xml(annoRootPath + './100009.xml')
    object_list = root.findall('object')
    count = object_list

    for i in range(0, count):






    # 移除object
    # for element in root.findall('object'):
    #     tag = element.tag
    #     attrib = element.attrib
    #     text = element.find('name').text
    #     print(tag, attrib, text)
    #     root.remove(element)
    # object_list = root.findall('object')
    # print(len(object_list))
    # for i in range(0, len(object_list)):



    # for obj in root.iter('object'):
    #     root.remove(obj)
    #     print(obj[0].text)
    #     # root.remove(obj)

    tree.write('test.xml')


if __name__ == '__main__':
    test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

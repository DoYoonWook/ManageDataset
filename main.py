import os
import pdb
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
from xml.etree.ElementTree import ElementTree, Element


def test():
    imgRootPath = './test_voc/images/'
    annoRootPath = './test_voc/annotations/'
    # for file in os.listdir(annoRootPath):
    #     domTree = parse(annoRootPath + file)
    #     root = domTree.documentElement

    # 从xml文件中读取，使用getroot()获取根节点，得到的是一个Element对象
    tree = ET.parse(annoRootPath + './100009.xml')
    print('tree', type(tree))
    root = tree.getroot()
    print('root', type(root))
    for element in root.findall('object'):
        tag = element.tag
        attrib = element.attrib
        text = element.find('name').text
        print(tag, attrib, text)

    for obj in root.iter('object'):
        root.remove(obj)
        print(obj[0].text)
        # root.remove(obj)

    tree.write('test.xml')


    # print(root[0][0].text)  # 子节点是嵌套的，我们可以通关索引访问特定的子节点











    # print(rootNode.nodeName)

    # objects = root.getElementsByTagName('object')
    # print('objects', type(objects))
    # for ob in objects:

        # print(nameList[0].childNodes[0].data)
        # bndbox = nameList.getchildren()
        # print(bndbox)




if __name__ == '__main__':
    test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

'''
把图片按照目标框的大小裁剪分类
并且改变voc下xml的数值

'''

from __future__ import division
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

from PIL import Image
import xml.dom.minidom
import numpy as np

import codecs


# ==由于minidom默认的writexml()函数在读取一个xml文件后，修改后重新写入如果加了newl='\n',会将原有的xml中写入多余的行
# 　 ==因此使用下面这个函数来代替
def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    writer.write(indent + "<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    # a_names.sort()
    sorted(a_names)

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
                and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s" % (newl))
        for node in self.childNodes:
            if node.nodeType is not minidom.Node.TEXT_NODE:
                node.writexml(writer, indent + addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))


minidom.Element.writexml = fixed_writexml


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' ----- folder created')
        return True
    else:
        print(path + ' ----- folder existed')
        return False


# ImgPath = 'C:/Users/Desktop/XML_try/img/'
# AnnoPath = 'C:/Users/Desktop/XML_try/xml/'
# ProcessedPath = 'C:/Users/Desktop/CropedVOC/'
ImgPath = './ok_voc_pretrain/images/'
AnnoPath = './ok_voc_pretrain/annotations/'
ProcessedPath = './wrap_voc/'

mkdir(ProcessedPath)
mkdir(ProcessedPath + 'annotations/')
mkdir(ProcessedPath + 'images/')

imagelist = os.listdir(ImgPath)

# 找到节点
# 保存需要保留的节点信息
# 删除全部节点
# 插入保存的节点
# 保存文件

# 对每张图片进行操作
for image in imagelist:
    image_pre, ext = os.path.splitext(image)
    imgfile = ImgPath + image
    xmlfile = AnnoPath + image_pre + '.xml'

    # ET_tree = ET.parse((xmlfile))
    # root = ET_tree.getroot()

    # 打开xml文件，并读取信息
    DomTree = xml.dom.minidom.parse(xmlfile)
    annotation = DomTree.documentElement

    # 获取xml中的filename
    filenamelist = annotation.getElementsByTagName('filename')  # [<DOM Element: filename at 0x381f788>]

    # 找到了一个图片中的所有objects，保存在objectList中
    # objects的父节点是root
    objectlist = annotation.getElementsByTagName('object')

    # 计算一张图片里面有几个object
    countObjects = 0

    # 对一张图片里面的所有objects逐一进行操作保留他们的信息到 对应的数组里面
    w_list = []
    h_list = []
    objectname_list = []

    for objects in objectlist:
        countObjects = countObjects + 1

        # 获取object的名字
        namelist = objects.getElementsByTagName('name')
        objectname = namelist[0].childNodes[0].data
        objectname_list.append(objectname)

        # 获取目标框
        bndbox = objects.getElementsByTagName('bndbox')
        cropboxes = []

        # 获取目标框的四个点
        for box in bndbox:
            x1_node = box.getElementsByTagName('xmin')
            x1 = float(x1_node[0].childNodes[0].data)
            y1_node = box.getElementsByTagName('ymin')
            y1 = float(y1_node[0].childNodes[0].data)
            x2_node = box.getElementsByTagName('xmax')
            x2 = float(x2_node[0].childNodes[0].data)
            y2_node = box.getElementsByTagName('ymax')
            y2 = float(y2_node[0].childNodes[0].data)

        # 新的图片的宽和高
        w = x2 - x1
        h = y2 - y1
        # print('w', w, 'h', h)

        # 把宽和高保存下来
        w_list.append(w)
        h_list.append(h)

        # 打开文件进行裁剪并保存
        img = Image.open(imgfile)
        cropedimg = img.crop((x1, y1, x2, y2))
        cropedimg.save('./wrap_voc/' + 'images/' +
                       image_pre + '_' + objectname + '_' + str(countObjects) + '.jpg')
        # cropedimg.show()

    # 开始对xml进行处理
    # 先清空原来到object
    for objects in objectlist:
        annotation.removeChild(objects)

    # temp用来计数
    temp = -1
    for num in range(countObjects):
        temp += 1

        newObjectList = annotation.getElementsByTagName('object')
        if(len(newObjectList) != 0):
            for temp_object_node in newObjectList:
                annotation.removeChild(temp_object_node)

        # 修改filename
        filename_node = annotation.getElementsByTagName('filename')
        filename_node[0].childNodes[0].data = image_pre + '_' + objectname_list[temp] + '_' + str(temp + 1) + '.jpg'
        # print(image_pre + '_' + objectname_list[temp] + '_' + str(temp + 1) + '.xml')

        # 修改width 和 height
        size_nodelist = annotation.getElementsByTagName('size')
        for size_node in size_nodelist:
            width_node = size_node.getElementsByTagName('width')
            width_node[0].childNodes[0].data = w
            height_node = size_node.getElementsByTagName('height')
            height_node[0].childNodes[0].data = h

        # 创立object标签
        objectDom = DomTree.createElement('object')

        # 创立object下面的子标签
        nameDom = DomTree.createElement('name')
        poseDom = DomTree.createElement('pose')
        truncatedDom = DomTree.createElement('truncated')
        difficultDom = DomTree.createElement('difficultDom')
        bndboxDom = DomTree.createElement('bndbox')

        # 给各个标签赋值
        nameDom.appendChild(DomTree.createTextNode(objectname_list[temp]))
        poseDom.appendChild(DomTree.createTextNode('Unspecified'))
        truncatedDom.appendChild(DomTree.createTextNode('0'))
        difficultDom.appendChild(DomTree.createTextNode('0'))

        # 创立bndbox的子标签
        xminDom = DomTree.createElement('xmin')
        yminDom = DomTree.createElement('ymin')
        xmaxDom = DomTree.createElement('xmax')
        ymaxDom = DomTree.createElement('ymax')

        # 给xmin 等赋值
        xminDom.appendChild(DomTree.createTextNode('0'))
        yminDom.appendChild(DomTree.createTextNode('0'))
        xmaxDom.appendChild(DomTree.createTextNode(str(w_list[temp])))
        ymaxDom.appendChild(DomTree.createTextNode(str(h_list[temp])))

        # 加入到bndbox标签下面
        bndboxDom.appendChild(xminDom)
        bndboxDom.appendChild(yminDom)
        bndboxDom.appendChild(xmaxDom)
        bndboxDom.appendChild(ymaxDom)

        # print('------------', image_pre, temp, objectname_list[temp])
        # 加入到object标签下面
        objectDom.appendChild(nameDom)
        objectDom.appendChild(poseDom)
        objectDom.appendChild(truncatedDom)
        objectDom.appendChild(difficultDom)
        objectDom.appendChild(bndboxDom)

        # 加入到annotation下面
        annotation.appendChild(objectDom)

        # 保存修改后的xml文件
        f = open('./wrap_voc/' + 'annotations/' +
                 image_pre + '_' + objectname_list[temp] + '_' + str(temp + 1) + '.xml', 'w')
        DomTree.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
        f.close()
        # print('./testDir/' + image_pre + '_' + str(countObjects) + '.xml')



# for num in range(10):
#     f = open('./testDir/' + str(num) + '.xml', 'w')
#     f.close()

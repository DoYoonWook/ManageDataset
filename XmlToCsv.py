import os
import xml.dom.minidom


def xml_to_csv():
    path_img = "VOC2007/JPEGImages"
    path_xml = "/home/tyx/Downloads/train-dataset/domain1/XML"

    xml_list = []
    for xml1 in os.listdir(path_xml):
        if xml1.endswith(".xml"):
            xml_list.append(xml1)

    csv_labels = open("domain1.csv", "w")
    for xml_file in xml_list:
        image_id, _ = os.path.splitext(xml_file)

        DomTree = xml.dom.minidom.parse(os.path.join(path_xml, xml_file))
        annotation = DomTree.documentElement
        objectlist = annotation.getElementsByTagName('object')
        for objects in objectlist:
            namelist = objects.getElementsByTagName('name')
            objectname = namelist[0].childNodes[0].data
            bndbox = objects.getElementsByTagName("bndbox")
            for box in bndbox:
                x1_list = box.getElementsByTagName('xmin')
                x1 = int(x1_list[0].childNodes[0].data)
                y1_list = box.getElementsByTagName('ymin')
                y1 = int(y1_list[0].childNodes[0].data)
                x2_list = box.getElementsByTagName('xmax')
                x2 = int(x2_list[0].childNodes[0].data)
                y2_list = box.getElementsByTagName('ymax')
                y2 = int(y2_list[0].childNodes[0].data)
            line = str("csv/images/" + image_id + ".jpg") + "," + str(x1) + "," + str(y1) \
                   + "," + str(x2) + "," + str(y2) + "," + objectname + "\n"
            print(line)
            csv_labels.write(line)
    csv_labels.close()


if __name__ == '__main__':
    xml_to_csv()

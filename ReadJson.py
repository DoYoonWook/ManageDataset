import json
import os
import shutil


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


# f = open('./ori_voc_COCO/annotations/train2017.json', encoding='utf-8')  # 打开‘product.json’的json文件

# 打开json文件
with open('./ok_voc_COCO/annotations/train2017.json', 'rb') as f:
    annotations_dic = json.load(f)


# print(json.loads(res))  # 把json串变成python的数据类型：字典
print(type(annotations_dic))
print(annotations_dic.keys())
# print(annotations_dic['annotations'])
print('len:', len(annotations_dic['images']))
# print(annotations_dic['images'][1]['id'])
# print(annotations_dic['annotations']['images'])
# print(annotations_dic['categories'])
# print(len(annotations_dic['annotations']))
# print(annotations_dic['annotations'][0])
# print(type(annotations_dic['annotations'][0]))
# print(annotations_dic['annotations'][0]['image_id'])
# print(type(annotations_dic['annotations']))
# print(annotations_dic['images'])

itemList = []
for item in annotations_dic['images']:
    print(item['id'])
    itemList.append(str(item['id']))



imgRootPath = './ok_voc_COCO/images/'
xmlRootPath = './ok_voc/annotations/'
imgSavePath = './ok_voc_pretrain/images/'
xmlSavePath = './ok_voc_pretrain/annotations/'

mkdir(imgSavePath)
mkdir(xmlSavePath)

fileList = os.listdir(imgRootPath)
for file in fileList:
    fileName0 = os.path.splitext(file)[0]

    if fileName0 in itemList:
        shutil.copy(imgRootPath + fileName0 + '.jpg', imgSavePath + fileName0 + '.jpg')
        shutil.move(xmlRootPath + fileName0 + '.xml', xmlSavePath + fileName0 + '.xml')
        # print(imgRootPath + fileName0 + '.jpg', imgSavePath + fileName0 + '.jpg')
        # print(xmlRootPath + fileName0 + '.xml', xmlSavePath + fileName0 + '.xml')

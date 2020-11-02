import os
import cv2
import json
import xml.etree.ElementTree as ElementTree
from shutil import copyfile

def pascalvoc_yolo(img_flderpath, label_flderpath, out_flderpath):
    ####load class from file
    classfile_path = os.path.join(label_flderpath, "classes.txt")
    outclassfile_path = os.path.join(out_flderpath, "classes.txt")
    readme_path = os.path.join(label_flderpath, "readme.txt")
    outreadme_path = os.path.join(out_flderpath, "readme.txt")
    class_list = []
    if os.path.exists(classfile_path):
        with open(classfile_path, "r") as cf:
            classes = cf.readlines()
        for cls in classes:
            class_list.append(cls.rstrip())
    if os.path.exists(readme_path):
        copyfile(readme_path, outreadme_path)
    ########read pascal voc and convert
    for fname in os.listdir(label_flderpath):
        if fname.lower() == "classes.txt" or fname.lower() == "readme.txt":
            continue
        fpath = os.path.join(label_flderpath, fname)
        xmltree = ElementTree.parse(fpath).getroot()
        filename = xmltree.find('filename').text
        imgname = fname.split(".xml")[0]+".jpg"
        imgpath = os.path.join(img_flderpath, imgname)
        img = cv2.imread(imgpath)
        if img is None:
            continue
        imgh, imgw,_ = img.shape
        outf = open(os.path.join(out_flderpath, imgname+".txt"), "w")
        for object_iter in xmltree.findall('object'):
            bndbox = object_iter.find("bndbox")
            cls = object_iter.find('name').text
            if not cls in class_list:
                class_list.append(cls)
            class_index = class_list.index(cls)
            xmin = int(bndbox.find("xmin").text)
            ymin = int(bndbox.find("ymin").text)
            xmax = int(bndbox.find("xmax").text)
            ymax = int(bndbox.find("ymax").text)
            w = xmax-xmin
            h = ymax-ymin
            cx = int(xmin+w/2)
            cy = int(ymin+h/2)
            cxs = float(cx/imgw)
            cys = float(cy/imgh)
            ws = float(w/imgw)
            hs = float(h/imgh)
#            print(str(class_index)+" "+str(cxs)+" "+str(cys)+" "+str(ws)+" "+str(hs))
            outf.write(str(class_index)+" "+str(cxs)+" "+str(cys)+" "+str(ws)+" "+str(hs)+"\n")
        outf.close()
    ########save class list to file
#    print(class_list)
    if not os.path.exists(outclassfile_path):
        with open(outclassfile_path, "w") as cf:
            for cls in class_list:
                cf.write(cls+"\n")
if __name__=="__main__":
    True
    pascalvoc_yolo("back_cmtnd_resized", "back_cmtnd_resized_label_pascal", "back_cmtnd_resized_label_yolo")
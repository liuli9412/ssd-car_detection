# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 12:37:25 2017

@author: liuli
"""

import json
import os
from PIL import Image

def endWith(s, *endstring):
    array = map(s.endswith,endstring)
    if True in array:
        return True
    else:
        return False
    
def load(filename):
    with open(filename,"r",encoding="UTF-8") as json_file:
        data = json.load(json_file)
        return data

path = ['sunny']
resize_height = 240
resize_width = 420
# 包含所有车辆和other里面的车辆
val_data_car_type = ["三轮车",'卡车','厢式车','中型乘用车','城市公交车','小型汽车','有轨电车','长途客车']
#包含Pedstrian、seated person、和other里面的行人
val_data_pedestrian_type = ["行人",'坐着的人']
#包含person on bike 和person on motorbike
val_data_bicycle_type = ['骑电动自行车/摩托车行人','骑自行车行人']
#4类别目前不添加数据，但是这个类别保留
val_data_other_type = []
val_data_type_name = [val_data_car_type,val_data_pedestrian_type,val_data_bicycle_type]
type_name_dic = {0:"Car",1:"Pes",2:"Bicycle"}
num = 0   #总数
small_box_num = {} #小框总数
all_types = {}
for i in path:
    for parents,dirs,filenames in os.walk(i):
        for filename in filenames:
            if endWith(filename,'.json'):
                num+=1
                print(num)
                json_file_path = os.path.join(parents,filename)
                
                
                file_name = filename[:-5]
                label_path = parents+'LABEL'
                print(label_path)
                if not os.path.exists(label_path):
                    os.mkdir(label_path)
                    
                label_name = file_name + '.txt'
                label_file_path = os.path.join(label_path,label_name)
                
                image_name = file_name + '.jpg'
                image_file_path = os.path.join(parents,image_name)
                #print(image_file_path)
                im = Image.open(image_file_path)
                ori_width = int(im.size[0])
                ori_height = int(im.size[1])
                #new_img = im.resize((resize_width,resize_height),Image.BILINEAR)
                #new_img.save(image_file_path)
                s = load(json_file_path)
                boxes_value = s["boxs"]
                lab_file = open(label_file_path,"w")
                for boxes in boxes_value:
                    val_data = boxes["val_data"]
                    cut = boxes["cut"] if 'cut' in boxes else "0"
                    if cut == None:
                        cut = '-1'
                    shade  = boxes["shade"] if "shade" in boxes else "0"
                    if shade == None:
                        shade = "-1"
                    if int(shade) >2 or int(cut) >3:
                        print (filename, cut, shade)
                        continue
                    if boxes["type"] not in all_types:
                        all_types[boxes["type"]] = 1
                    else:
                        all_types[boxes["type"]] += 1
                    for (index, item) in enumerate(val_data_type_name):
                        if boxes["type"] in item:
                            box_class =  str(index+1)
                            w    = boxes["w"] 
                            h    = boxes["h"]
                            x_top= boxes["x"] if boxes["x"] > 0 else 0
                            y_top= boxes["y"] if boxes["y"] > 0 else 0
                            x_max= (x_top+w) if (x_top+w) < ori_width else ori_width
                            y_max= (y_top+h) if (y_top+h) < ori_height else ori_height
                            if(w*resize_width/ori_width <8 or h*resize_height/ori_height<8):
                                if box_class not in small_box_num:
                                    small_box_num[box_class] = 1
                                else:
                                    small_box_num[box_class] += 1
                                print (small_box_num)
                                continue 
                            else:
                                msg = box_class + " " +  str(x_top) + " "+ str(y_top) + " "+  str(x_max) + " " + str(y_max) +'\n' 
                                lab_file.write(msg)
                lab_file.close()
with open("all_types.json","w") as f:
    json.dump(all_types,f)
                        
                    
                    
                
                

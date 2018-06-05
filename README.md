# ssd-car_detection
基于改进SSD的车辆行人检测
![Image text](https://github.com/GeekLee95/ssd-car_detection/blob/master/%E6%95%B0%E6%8D%AE%E5%8F%8A%E6%A8%A1%E5%9E%8B/%E9%A2%84%E6%B5%8B/data0orig_Result/0000000011.png) 
1. 数据预处理文件夹
   parse_boundingbox_from_josn.py为提取bbox脚本
   删除了原始数据中框尺寸小于最小感受野的大小的框，生成的是txt格式的bbox标注

   create_list.sh 和create_data.sh 为生成LMDB数据的脚本
   
2. 输入图片大小为240x420

3. 当没有pretrained model进行训练时，先将三部分的惩项系数均设置成1,等map上去后再调整相应的罚项系数。

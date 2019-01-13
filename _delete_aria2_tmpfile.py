#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

clean_dir = input("输入工作目录(enter 默认当前)：")
if clean_dir == '' :
    clean_dir = os.getcwd()
    print("默认当前路径： %s "% os.getcwd())
else:
    try:
        os.chdir(clean_dir)
    except FileNotFoundError:
        print("ERROR:%s not dir!" % clean_dir)
        sys.exit(0)
print("扫描 %s 目录以及子目录......" % clean_dir)

#遍历，如果文件后缀为.arai2,删除
def remove_aria2file(clean_dir):
    #获取目录下文件列表
    path_dir = os.listdir(clean_dir)
    for file in path_dir:
        tmp_path = os.path.join(clean_dir,file)
        #print(tmp_path)
        if not os.path.isdir(tmp_path):
            suffix = os.path.splitext(file)[-1]
            if suffix == ".aria2":
                print("aria2 download tmp file %s remove!" % tmp_path)
                os.remove(tmp_path)
            #else:
                #print("not file")
        else:
            print("子目录：%s" % tmp_path)
            remove_aria2file(tmp_path)


remove_aria2file(clean_dir)
print("over!")
sys.exit(0)


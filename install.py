#!/bin/python
#coding:utf-8
import os
import subprocess
import sys
import time

def install(path):
    for root,path,files in os.walk(path):
        for f in files:
            installfile = root + "/" + f
            cmd = "kubectl apply -f {installfile}".format(installfile=installfile)
            print(cmd)
            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            out = p.stdout.read()
            print(out)
            time.sleep(1)


# 安装文件
path = "./manifest1.3"
install(path)

# 安装patch
patchPath = "./patch"
install(patchPath)
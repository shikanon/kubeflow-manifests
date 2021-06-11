#!/bin/python
#coding:utf-8
import os
import subprocess
import sys
import time

def uninstall(path):
    for root,path,files in os.walk(path):
        files = sorted(files, reverse=True)  # delete yaml by reverse order
        for f in files:
            installfile = root + "/" + f
            cmd = "kubectl delete -f {installfile}".format(installfile=installfile)
            print('========', cmd, '========')
            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            out = p.stdout.read()
            print(out)
            time.sleep(1)


if __name__ == '__main__':
    path = "./manifest1.3"
    uninstall(path)

#!/bin/python
#coding:utf-8

import os
import shlex
import yaml
from yaml import CLoader
from replace import replaceImage
import subprocess


mainfile = "kustomization.yaml"

with open(mainfile, "r") as fr:
    kustomizefile = yaml.load(fr,Loader=CLoader)

n = 0
for path in kustomizefile['resources']:
    n = n + 1
    abspath = os.path.abspath(path)
    abspath = abspath.replace("\\","/")
    filename = "-".join([path.split("/")[2]]+path.split("/")[-2:])
    cmd = "kustomize build --load_restrictor=none {path}".format(path=path)
    print(cmd)
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    out = p.stdout.read()
    if out == "":
        raise ValueError(cmd)
    filename = str(n).zfill(3) + "-" + filename +".yaml"
    out = replaceImage(out.decode("utf-8"))
    with open("file/"+ filename, "w", encoding="utf-8") as fw:
        fw.write(out)
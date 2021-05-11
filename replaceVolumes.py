#!/bin/python
#coding:utf-8
import os
import yaml

def findVolumeDeployment(content):
    crs = content.split("---\n")
    images = dict()
    for cr in crs:
        if len(cr) < 0:
            continue
        obj = yaml.load(cr, yaml.CLoader)
        if obj is None or "kind" not in obj:
            continue
        if obj["kind"] == "Deployment":
            specs = obj["spec"]["template"]["spec"]
            if "volumes" in specs:
                for v in specs["volumes"]:
                    if "persistentVolumeClaim" in v:
                        del v["persistentVolumeClaim"]
                        v ["emptyDir"] = dict()
                        yield v["name"],cr


def savePatchPath(content,filename):
    path = "./patch/" + filename + ".yaml"
    with open(path,"w") as fw:
        fw.write(content)


if __name__ == "__main__":
    for root,path,files in os.walk("./file"):
        for f in files:
            findfile = root + "/" + f
            with open(findfile,"r",encoding="utf-8") as fr:
                for name,cr in findVolumeDeployment(fr.read()):
                    print(name)
                    print(cr)
                    savePatchPath(cr, name)
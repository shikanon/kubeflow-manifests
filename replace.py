#!/bin/python
#coding:utf-8
import yaml
import os
import subprocess
import sys
import json


IMAGE_PREFIX = "registry.cn-shenzhen.aliyuncs.com/tensorbytes/"


def getNewImage(image, prefix):
    # get hash of image
    cmd = "docker inspect "+image
    print(cmd)
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    out = p.stdout.read()
    out = json.loads(out)[0]
    imagehash = out["Id"].split(":")[-1][:5]
    pending = "-" + imagehash
    # change image to new tag
    app = image.split("/")[-1]
    if len(image.split("/")) > 1:
        org = image.split("/")[-2]
        app = org + "-" + app
    if ":" in app:
        if "@sha256:" in app:
            appname = app.split("@")[0]
            appversion = "special"
        else:
            appversion = app.split(":")[-1]
            appname = app.split(":")[0]
    else:
        appname = app
        appversion = "latest"
    newImage = prefix + appname + ":" + appversion + pending
    return newImage


def findDeploymentImage(content):
    crs = content.split("---\n")
    images = dict()
    for cr in crs:
        if len(cr) < 0:
            continue
        obj = yaml.load(cr, yaml.CLoader)
        if obj is None or "kind" not in obj:
            continue
        if obj["kind"] == "Deployment" or obj["kind"] == "StatefulSet":
            containers = obj["spec"]["template"]["spec"]["containers"]
            for c in containers:
                obj_image = c["image"]
                cmdPull = "docker pull {image}".format(image=obj_image)
                os.system(cmdPull)
                newimage = getNewImage(obj_image, IMAGE_PREFIX)
                images[obj_image] = newimage
    return images


def replaceImage(content):
    imageMap = findDeploymentImage(content)
    for image in imageMap:
        content = content.replace(image,imageMap[image])
        logAndPushImage(imageMap)
    return content

def logAndPushImage(imageMap):
    with open("images.log","a") as fw:
        for image in imageMap:
            # pull image
            cmdPull = "docker pull {image}".format(image=image)
            # tag image
            cmdTag = "docker tag {oldimage} {newimage}".format(oldimage=image, newimage=imageMap[image])
            # push new images
            cmdPush = "docker push {image}".format(image=imageMap[image])
            print(cmdPush)
            os.system(cmdTag)
            os.system(cmdPush)
            # log
            line = image + "\t" + imageMap[image]
            fw.write(line+"\n")


if __name__ == "__main__":
    with open("./file/023-jupyter-overlays-kubeflow.yaml") as fr:
        images = replaceImage(fr.read())
        # print(images)
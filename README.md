# Kubeflow一键安装

国内由于镜像网络问题，Kubeflow 通常安装都是各种磕磕碰碰，以一颗为广大人民谋福利的心，这里提供国内镜像版(阿里云镜像/dockerhub)的一键安装：

#### 安装步骤

**1.生成yaml**
```
python run.py
```

**2.启动**
```
cd yaml
kubectl apply -f .
```

*注：如果需要用local-path文件夹下的yaml文件生成：`kubectl apply -f local-path-storage.yaml`*

**3.查看结果**
```
kubectl get pod -nkubeflow
```
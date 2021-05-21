# Kubeflow安装及使用教程（中国版）

由于国内网络问题，Kubeflow 通常安装都是各种磕磕碰碰，以一颗为广大人民谋福利的心，这里提供中国的本地镜像版(阿里云镜像/dockerhub)的**安装**。
同时这里汇总了一些kubeflow的中文教程资料供大家参考。

## Kubeflow 使用教程
- [kubeflow安装](/README.md)
- [kubeflow各组件介绍](/docs/introduction.md)

## 安装步骤

### 安装k8s

如果已经有k8s集群，这一步可以跳过，直接到[kubeflow安装](https://github.com/shikanon/kubeflow-manifests#%E5%AE%89%E8%A3%85kubeflow)。

**kind安装k8s集群**

下载[kind工具](https://github.com/kubernetes-sigs/kind/tags)

使用kind安装k8s集群：

```bash
$ kind create cluster --config=kind/kind-config.yaml --name=kubeflow --image=kindest/node:v1.16.9
```

启动成功后可以看到开了一个30000端口：
```bash
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS         PORTS                                                 NAMES
5f67af713e28   kindest/node:v1.19.1   "/usr/local/bin/entr…"   3 minutes ago   Up 3 minutes   0.0.0.0:30000->30000/tcp, 127.0.0.1:56682->6443/tcp   kubeflow-control-plane
```

由于 kubeflow 实验组件较多，最好准备机器的最低配置能够大于*CPU8核,内存32G*以上。

### 安装kubeflow

**2.启动**
```bash
$ python install.py
```

等待镜像拉取，由于涉及的镜像比较多，要20~30分钟左右，可以通过命令查看是否就绪：

**3.查看结果**
```
$ kubectl get pod -nkubeflow
NAME                                                        READY   STATUS    RESTARTS   AGE
admission-webhook-deployment-6fb9d65887-pzvgc               1/1     Running   0          19h
cache-deployer-deployment-7558d65bf4-jhgwg                  2/2     Running   1          3h54m
cache-server-c64c68ddf-lx7xq                                2/2     Running   0          3h54m
centraldashboard-7b7676d8bd-g2s8j                           1/1     Running   0          4h46m
jupyter-web-app-deployment-66f74586d9-scbsm                 1/1     Running   0          3h4m
katib-controller-77675c88df-mx4rh                           1/1     Running   0          19h
katib-db-manager-646695754f-z797r                           1/1     Running   0          19h
katib-mysql-5bb5bd9957-gbl5t                                1/1     Running   0          19h
katib-ui-55fd4bd6f9-r98r2                                   1/1     Running   0          19h
kfserving-controller-manager-0                              2/2     Running   0          19h
kubeflow-pipelines-profile-controller-5698bf57cf-dhtsj      1/1     Running   0          3h52m
metacontroller-0                                            1/1     Running   0          4h52m
metadata-envoy-deployment-76d65977f7-rmlzc                  1/1     Running   0          4h52m
metadata-grpc-deployment-697d9c6c67-j6dl2                   2/2     Running   3          4h52m
metadata-writer-58cdd57678-8t6gw                            2/2     Running   1          4h52m
minio-6d6784db95-tqs77                                      2/2     Running   0          4h45m
ml-pipeline-85fc99f899-plsz2                                2/2     Running   1          4h52m
ml-pipeline-persistenceagent-65cb9594c7-xvn4j               2/2     Running   1          4h52m
ml-pipeline-scheduledworkflow-7f8d8dfc69-7wfs4              2/2     Running   0          4h52m
ml-pipeline-ui-5c765cc7bd-4r2j7                             2/2     Running   0          4h52m
ml-pipeline-viewer-crd-5b8df7f458-5b8qg                     2/2     Running   1          4h52m
ml-pipeline-visualizationserver-56c5ff68d5-92bkf            2/2     Running   0          4h52m
mpi-operator-789f88879-n4xms                                1/1     Running   0          19h
mxnet-operator-7fff864957-vq2bg                             1/1     Running   0          19h
mysql-56b554ff66-kd7bd                                      2/2     Running   0          4h45m
notebook-controller-deployment-74d9584477-qhpp8             1/1     Running   0          19h
profiles-deployment-67b4666796-k7t2h                        2/2     Running   0          19h
pytorch-operator-fd86f7694-dxbgf                            2/2     Running   0          19h
tensorboard-controller-controller-manager-fd6bcffb4-k9qvx   3/3     Running   1          19h
tensorboards-web-app-deployment-78d7b8b658-dktc6            1/1     Running   0          19h
tf-job-operator-7bc5cf4cc7-gk8tz                            1/1     Running   0          19h
volumes-web-app-deployment-68fcfc9775-bz9gq                 1/1     Running   0          19h
workflow-controller-566998f76b-2v2kq                        2/2     Running   1          4h52m
xgboost-operator-deployment-5c7bfd57cc-9rtq6                2/2     Running   1          19h
```

如果所有pod 都running了表示安装完了。

*注：除了kubeflow命名空间，该一键安装工具也会安装istio,knative,因此也要保证这两个命名空间下的服务全部running*

全部pod running后，可以访问本地的30000端口（istio-ingressgateway设置了nodeport为30000端口），就可以看到登录界面了：
![](/example/dex登录界面.png)

输入账号密码即可登录，这里的账号密码可以通过`patch/auth.yaml`进行更改。
默认的用户名是`admin@example.com`，密码是`password`

登录后进入kubeflow界面：
![](/example/kubeflow-dashboardcenter.png)

### 删除kubeflow资源

```bash
 kind delete cluster --name kubeflow
```


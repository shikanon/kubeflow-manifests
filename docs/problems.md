# 问题汇总 

1. 没有 namespace, Experiments 报错。

这种是 `profile` 设置问题。

由于官方使用的是`user@example.com`创建命名空间`kubeflow-user-example-com`，这里在`patch`改成了`admin@example.com`
，当命名空间已经创建后，就会报错，一般我们查看 profiles-deployment 日志，会看到:
```bash
2021-05-19T06:41:43.069Z        INFO    controllers.Profile     namespace already exist, but not owned by profile creator admin@example.com     {"profile": "/kubeflow-user-example-com"}
2021-05-19T06:41:43.077Z        DEBUG   controller      Successfully Reconciled {"reconcilerGroup": "kubeflow.org", "reconcilerKind": "Profile", "controller": "profile", "name": "kubeflow-user-example-com", "namespace": ""}
```
这时候只需要删除`profile`命名空间`kubeflow-user-example-com`,重新生产`profile`即可。
```bash
kubectl delete -f patch/auth.yaml
kubectl delete ns kubeflow-user-example-com
kubectl apply -f patch/auth.yaml
```

2. 运行 pipeline 报错，错误显示`xxx is not implemented in the k8sapi executor`

这个错误是由于 kind 集群创建的 k8s 集群容器运行时用的containerd，而workflow默认的pipeline执行器是docker，因此有些特性不兼容。如果你的 k8s 集群是自己基于docker runtime 搭建的，可以将`patch/workflow-controller.yaml`的`containerRuntimeExecutor`改为`docker`，这样就不存在兼容性问题了。

详细见：

https://github.com/argoproj/argo-workflows/issues/2685#issuecomment-613632304
https://argoproj.github.io/argo-workflows/workflow-executors/
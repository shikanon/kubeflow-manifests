# 开发文档

这里主要介绍如何构建这个项目的。主要分为几步：替换镜像，重新打标签上传到私有镜像仓库，生成安装文档。

运行命令：
```bash
python pre-install.py
python install.py
```

## 实现原理

### 预处理

通过 `kustomize build --load_restrictor=none` 生成镜像目标yaml 文件

### 替换镜像

替换镜像主要是 `replace.py`实现，主要从 deployment, statefulset 找到镜像字段，重新打标签替换成新的镜像仓库地址，push上传到私有镜像仓库

### 安装文件

运行`python install.py` 安装文件。

## PATCH文件

patch文件主要针对官方yaml安装使用过程中的一些问题打的补丁

### 鉴权问题
`auth.yaml` 主要用于创建用户自己的账号，用户名`admin@example.com`，密码`password`

### istio报istio-token找不到

主要是由于istio的JWT策略用到第三方鉴权，有些k8s版本不支持，可以将isito中的 `third-party-jwt` 改成 `first-party-jwt`，详细见`cluster-local-gateway.yaml`,`istio-ingressgateway.yaml`,`istiod.yaml`。

### 创建jupyter的时候返回 Could not find CSRF cookie XSRF-TOKEN 错误

主要是由于jupyter-web-app的安全验证策略导致的，详细见https://github.com/kubeflow/kubeflow/issues/5803
解决方案环境变量加上`APP_SECURE_COOKIES=false`,修改见`jupyter-web-app.yaml`

### 解决docker.sock not found 问题

因为 kind 使用的 containerd 作为容器运行时，而 argo workflow 默认 Workflow Executors使用的是 docker ，他会尝试挂载宿主机的 `docker.sock`，如果不存在就会报错，这里尝试将`workflow-controller-configmap`的`containerRuntimeExecutor` 改为 `k8sapi` 更换 Workflow Executors 来解决。详细见：https://argoproj.github.io/argo-workflows/workflow-executors/
# Introduction

---

![](https://shikanon.com/img/kubeflow/kubeflow-dashboardcenter.png)

可以看到新版的kubeflow多了很多功能。

这里按模块介绍下 Kubeflow 的几个核心组件。
- Notebook Servers，作为一个管理线上交互实验的记录工具，可以帮助算法人员快速完成算法实验，同时notebook server 提供了统一的文档管理能力。
- AutoML，提供自动化的服务，对特征处理、特征选择、模型选择、模型参数的配置、模型训练和评估等方面，实现了全自动建模，降低算法人员手动实验次数。
- Pipeline，提供一个算法流水线的工程化工具，将算法各流程模块以拓扑图的形式组合起来，同时结合 argo 可以实现 MLOps。
- Serverless，将模型直接发布成一个对外的服务，缩短从实验到生产的路径。

![](https://shikanon.com/img/kubeflow/kubeflow组件.png)

## Notebook Servers

notebook 可以说是做机器学习最喜欢用到的工具了，完美的将动态语言的交互性发挥出来，kubeflow 提供了 jupyter notebook 来快速构建云上的实验环境，这里以一个我们自定义的镜像为例：

![](https://shikanon.com/img/kubeflow/kubeflow-create-notebook.png)

我们创建了一个`test-for-jupyter`名字的镜像，配置了一个 tensorflow 的镜像，点击启动，我们可以看到在`kubeflow-user-example-com`命名空间下已经创建我们的应用了：
```bash
kubectl get po -nkubeflow-user-example-com
NAME                                               READY   STATUS            RESTARTS   AGE
ml-pipeline-ui-artifact-6d7ffcc4b6-9kxkk           2/2     Running           0          48m
ml-pipeline-visualizationserver-84d577b989-5hl46   2/2     Running           0          48m
test-for-jupyter-0                                 0/2     PodInitializing   0          44s
```

![](https://shikanon.com/img/kubeflow/notebook-server-ui.png)

创建完成后点击 connect 就可以进入我们创建的应用界面中了

![](https://shikanon.com/img/kubeflow/jupterlab-webui.png)
![](https://shikanon.com/img/kubeflow/jupterlab-web-run-code.png)

在 jupyterlab 环境中开发人员可以很方便的进行算法实验，同时由于运行在云上利用 k8s api甚至可以很方便构建k8s资源，比如通过 kfserving 创建一个ML服务。

![](https://shikanon.com/img/kubeflow/jupyter-kfserving.png)


## AutoML

AutoML 是机器学习比较热的领域，主要用来模型自动优化和超参数调整，这里其实是用的 Katib来实现的，一个基于k8s的 AutoML 项目，详细见https://github.com/kubeflow/katib。

Katib 主要提供了 超参数调整(Hyperparameter Tuning)，早停法(Early Stopping)和神经网络架构搜索(Neural Architecture Search)

这里以一个随机搜索算法为例：
```yaml
apiVersion: "kubeflow.org/v1beta1"
kind: Experiment
metadata:
  namespace: kubeflow-user-example-com
  name: random-example
spec:
  objective:
    type: maximize
    goal: 0.99
    objectiveMetricName: Validation-accuracy
    additionalMetricNames:
      - Train-accuracy
  algorithm:
    algorithmName: random
  parallelTrialCount: 3
  maxTrialCount: 12
  maxFailedTrialCount: 3
  parameters:
    - name: lr
      parameterType: double
      feasibleSpace:
        min: "0.01"
        max: "0.03"
    - name: num-layers
      parameterType: int
      feasibleSpace:
        min: "2"
        max: "5"
    - name: optimizer
      parameterType: categorical
      feasibleSpace:
        list:
          - sgd
          - adam
          - ftrl
  trialTemplate:
    primaryContainerName: training-container
    trialParameters:
      - name: learningRate
        description: Learning rate for the training model
        reference: lr
      - name: numberLayers
        description: Number of training model layers
        reference: num-layers
      - name: optimizer
        description: Training model optimizer (sdg, adam or ftrl)
        reference: optimizer
    trialSpec:
      apiVersion: batch/v1
      kind: Job
      spec:
        template:
          spec:
            containers:
              - name: training-container
                image: docker.io/kubeflowkatib/mxnet-mnist:v1beta1-45c5727
                command:
                  - "python3"
                  - "/opt/mxnet-mnist/mnist.py"
                  - "--batch-size=64"
                  - "--lr=${trialParameters.learningRate}"
                  - "--num-layers=${trialParameters.numberLayers}"
                  - "--optimizer=${trialParameters.optimizer}"
            restartPolicy: Never
```

这里以一个简单的神经网络为例，该程序具有三个参数 lr, num-layers, optimizer，采用的算法是随机搜索，目标是最大化准确率(accuracy)。

可以直接在界面中填上yaml文件，然后提交，完成后会生成一张各参数和准确率的关系图和训练列表：
![](https://shikanon.com/img/kubeflow/katib-tune-hyperparameter.png)
![](https://shikanon.com/img/kubeflow/katib-tune-hyperparameter-training.png)

## Experiments and Pipelines

experiments 为我们提供了一个可以创建实验空间功能， `pipeline` 定义了算法组合的模板，通过 `pipeline` 我们可以将算法中各处理模块按特定的拓扑图的方式组合起来。

这里可以看看官方提供的几个 pipeline 例子：
![](https://shikanon.com/img/kubeflow/kubeflow-pipeline-example.png)
![](https://shikanon.com/img/kubeflow/kubeflow-pipeline-example2.png)

kubeflow `pipeline` 本质是基于 argo `workflow` 实现，**由于我们的kubeflow是基于kind上构建的，容器运行时用的containerd，而workflow默认的pipeline执行器是docker，因此有些特性不兼容**，这块可以见 argo workflow 官方说明：https://argoproj.github.io/argo-workflows/workflow-executors/。
这里我是把 workflow 的 `containerRuntimeExecutor` 改成了 `k8sapi`。但 `k8sapi` 由于在 workflow 是二级公民，因此有些功能不能用，比如 kubeflow pipeline 在 input/output 的 artifacts 需要用到 `docker cp` 命令，可以参考这个issue: https://github.com/argoproj/argo-workflows/issues/2685#issuecomment-613632304

由于以上原因 kubeflow 默认给的几个案例并没有用 volumes 是无法在 kind 中运行起来，这里我们基于 argo workflow 语法自己实现一个 `pipeline`

### 基于pipeline构建一个的工作流水

**第一步，构建一个 workflow pipeline 文件：**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: kubeflow-test-
spec:
  entrypoint: kubeflow-test
  templates:
  - name: kubeflow-test
    dag:
      tasks:
      - name: print-text
        template: print-text
        dependencies: [repeat-line]
      - {name: repeat-line, template: repeat-line}
  - name: repeat-line
    container:
      args: [--line, Hello, --count, '15', --output-text, /gotest/outputs/output_text/data]
      command:
      - sh
      - -ec
      - |
        program_path=$(mktemp)
        printf "%s" "$0" > "$program_path"
        python3 -u "$program_path" "$@"
      - |
        def _make_parent_dirs_and_return_path(file_path: str):
            import os
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            return file_path

        def repeat_line(line, output_text_path, count = 10):
            '''Repeat the line specified number of times'''
            with open(output_text_path, 'w') as writer:
                for i in range(count):
                    writer.write(line + '\n')

        import argparse
        _parser = argparse.ArgumentParser(prog='Repeat line', description='Repeat the line specified number of times')
        _parser.add_argument("--line", dest="line", type=str, required=True, default=argparse.SUPPRESS)
        _parser.add_argument("--count", dest="count", type=int, required=False, default=argparse.SUPPRESS)
        _parser.add_argument("--output-text", dest="output_text_path", type=_make_parent_dirs_and_return_path, required=True, default=argparse.SUPPRESS)
        _parsed_args = vars(_parser.parse_args())

        _outputs = repeat_line(**_parsed_args)
      image: python:3.7
      volumeMounts:
      - name: workdir
        mountPath: /gotest/outputs/output_text/
    volumes:
      - name: workdir
        persistentVolumeClaim:
          claimName: kubeflow-test-pv
    metadata:
      annotations: 
  - name: print-text
    container:
      args: [--text, /gotest/outputs/output_text/data]
      command:
      - sh
      - -ec
      - |
        program_path=$(mktemp)
        printf "%s" "$0" > "$program_path"
        python3 -u "$program_path" "$@"
      - |
        def print_text(text_path): # The "text" input is untyped so that any data can be printed
            '''Print text'''
            with open(text_path, 'r') as reader:
                for line in reader:
                    print(line, end = '')

        import argparse
        _parser = argparse.ArgumentParser(prog='Print text', description='Print text')
        _parser.add_argument("--text", dest="text_path", type=str, required=True, default=argparse.SUPPRESS)
        _parsed_args = vars(_parser.parse_args())

        _outputs = print_text(**_parsed_args)
      image: python:3.7
      volumeMounts:
      - name: workdir
        mountPath: /gotest/outputs/output_text/
    volumes:
      - name: workdir
        persistentVolumeClaim:
          claimName: kubeflow-test-pv
    metadata:
      annotations: 
```

argo workflow 的语法可以参考：https://argoproj.github.io/argo-workflows/variables/

这里我们定义了两个任务 repeat-line 和 print-text, repeat-line 任务会将生产结果写入 `kubeflow-test-pv` 的 PVC 中， print-text 会从 PVC 中读取数据输出到 stdout。

这里由于用到 PVC，我们需要先在集群中创建一个`kubeflow-test-pv`的PVC:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: kubeflow-test-pv
  namespace: kubeflow-user-example-com
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 128Mi
```


**第二步，定义好 pipeline 文件后可以创建pipeline：**

![](https://shikanon.com/img/kubeflow/kubeflow-upload-pipeline.png)

**第三步，启动一个pipeline：**

![](https://shikanon.com/img/kubeflow/kubeflow-crate-pipeline.png)

启动 pipeline 除了单次运行模式 one-off，也支持定时器循环模式 Recurring，这块可以根据自己的需求确定。

**查看运行结果：**

![](https://shikanon.com/img/kubeflow/kbueflow-pipeline-result.png)

运行完后，可以将实验进行归档(Archived)。



## 关于 MLOps 的一点思考

我们来看一个简单的 ML 运作流程：
![](https://shikanon.com/img/kubeflow/google-mlops.svg)

这是一个 google 提供的 level 1 级别的机器学习流水线自动化，整个流水线包括以下几部分：
- 构建快速算法实验的环境(experimentation)，这里的步骤已经过编排，各个步骤之间的转换是自动执行的，这样可以快速迭代实验，并更好地准备将整个流水线移至生产环境，在这个环境中算法研究员只进行模块内部的工作。
- 构建可复用的生产环境流水线，组件的源代码模块化，实验环境模块化流水线可以直接在 staging 环境和 production 环境中使用。
- 持续交付模型，生产环境中的机器学习流水线会向使用新数据进行训练的新模型持续交付预测服务。

基于上述功能描述我们其实可以基于 kubeflow 的 `pipeline` 和 `kfserving` 功能轻松实现一个简单的 MLOps 流水线发布流程。不过，值得注意的是，DevOps 本身并不仅仅是一种技术，同时是一种工程文化，所以在实践落地中需要团队各方的协同分阶段的落地。这块可以参考[《MLOps: Continuous delivery and automation pipelines in machine learning》](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)和[《Hidden Technical Debt in Machine Learning Systems》](https://papers.nips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)


# 参考文献
- https://www.tensorflow.org/tutorials/quickstart/beginner
- https://github.com/dexidp/dex
- https://github.com/kubeflow/kfserving/tree/master/docs
- https://argoproj.github.io/argo-workflows/workflow-executors/
- https://github.com/shikanon/kubeflow-manifests
- https://argoproj.github.io/argo-workflows/variables/
- https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
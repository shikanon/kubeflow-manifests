# coding:utf-8

import os

grc_image = [
"gcr.io/kubeflow-images-public/ingress-setup:latest",
"gcr.io/kubeflow-images-public/admission-webhook:v20190520-v0-139-gcee39dbc-dirty-0d8f4c",
"gcr.io/kubeflow-images-public/kubernetes-sigs/application:1.0-beta",
"gcr.io/kubeflow-images-public/centraldashboard:v20190823-v0.6.0-rc.0-69-gcb7dab59",
"gcr.io/kubeflow-images-public/jupyter-web-app:9419d4d",
"gcr.io/kubeflow-images-public/katib/v1alpha2/katib-controller:v0.6.0-rc.0",
"gcr.io/kubeflow-images-public/katib/v1alpha2/katib-manager:v0.6.0-rc.0",
"gcr.io/kubeflow-images-public/katib/v1alpha2/katib-manager-rest:v0.6.0-rc.0",
"gcr.io/kubeflow-images-public/katib/v1alpha2/suggestion-bayesianoptimization:v0.6.0-rc.0",
"gcr.io/kubeflow-images-public/katib/v1alpha2/suggestion-grid:v0.6.0-rc.0",
"gcr.io/kubeflow-images-public/katib/v1alpha2/suggestion-hyperband:v0.6.0-rc.0",
"gcr.io/kubeflow-images-public/katib/v1alpha2/suggestion-nasrl:v0.6.0-rc.0",
"gcr.io/kubeflow-images-public/katib/v1alpha2/suggestion-random:v0.6.0-rc.0",
"gcr.io/kubeflow-images-public/katib/v1alpha2/katib-ui:v0.6.0-rc.0",
"gcr.io/kubeflow-images-public/metadata:v0.1.8",
"gcr.io/kubeflow-images-public/metadata-frontend:v0.1.8",
"gcr.io/ml-pipeline/api-server:0.1.23",
"gcr.io/ml-pipeline/persistenceagent:0.1.23",
"gcr.io/ml-pipeline/scheduledworkflow:0.1.23",
"gcr.io/ml-pipeline/frontend:0.1.23",
"gcr.io/ml-pipeline/viewer-crd-controller:0.1.23",
"gcr.io/kubeflow-images-public/notebook-controller:v20190603-v0-175-geeca4530-e3b0c4",
"gcr.io/kubeflow-images-public/profile-controller:v20190619-v0-219-gbd3daa8c-dirty-1ced0e",
"gcr.io/kubeflow-images-public/kfam:v20190612-v0-170-ga06cdb79-dirty-a33ee4",
"gcr.io/kubeflow-images-public/pytorch-operator:v1.0.0-rc.0",
"gcr.io/google_containers/spartakus-amd64:v1.1.0",
"gcr.io/kubeflow-images-public/tf_operator:v0.6.0.rc0",
"gcr.io/arrikto/kubeflow/oidc-authservice:v0.2",
"gcr.io/kubeflow-images-public/katib/v1alpha2/metrics-collector:v0.1.2-alpha-289-g14dad8b"
]

ali_image = [
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.ingress-setup:latest",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.admission-webhook:v20190520-v0-139-gcee39dbc-dirty-0d8f4c",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.kubernetes-sigs.application:1.0-beta",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.centraldashboard:v20190823-v0.6.0-rc.0-69-gcb7dab59",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.jupyter-web-app:9419d4d",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.katib-controller:v0.6.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.katib-manager:v0.6.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.katib-manager-rest:v0.6.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.suggestion-bayesianoptimization:v0.6.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.suggestion-grid:v0.6.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.suggestion-hyperband:v0.6.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.suggestion-nasrl:v0.6.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.suggestion-random:v0.6.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.katib-ui:v0.6.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.metadata:v0.1.8",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.metadata-frontend:v0.1.8",
"registry.cn-shenzhen.aliyuncs.com/shikanon/ml-pipeline.api-server:0.1.23",
"registry.cn-shenzhen.aliyuncs.com/shikanon/ml-pipeline.persistenceagent:0.1.23",
"registry.cn-shenzhen.aliyuncs.com/shikanon/ml-pipeline.scheduledworkflow:0.1.23",
"registry.cn-shenzhen.aliyuncs.com/shikanon/ml-pipeline.frontend:0.1.23",
"registry.cn-shenzhen.aliyuncs.com/shikanon/ml-pipeline.viewer-crd-controller:0.1.23",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.notebook-controller:v20190603-v0-175-geeca4530-e3b0c4",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.profile-controller:v20190619-v0-219-gbd3daa8c-dirty-1ced0e",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.kfam:v20190612-v0-170-ga06cdb79-dirty-a33ee4",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.pytorch-operator:v1.0.0-rc.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/google_containers.spartakus-amd64:v1.1.0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.tf_operator:v0.6.0.rc0",
"registry.cn-shenzhen.aliyuncs.com/shikanon/arrikto.kubeflow.oidc-authservice:v0.2",
"registry.cn-shenzhen.aliyuncs.com/shikanon/kubeflow-images-public.katib.v1alpha2.metrics-collector:v0.1.2-alpha-289-g14dad8b"
]

for i in range(len(grc_image)):
    cmd = "docker tag %s %s"%(grc_image[i], ali_image[i])
    print(cmd)
    os.system(cmd)
    cmd = "docker push %s"%ali_image[i]
    print(cmd)
    os.system(cmd)

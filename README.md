# 使用方法


```shell
python3 k8s_image_save.py
```

- 脚本执行前提是需要安装 docker 和 kubeadm 命令
- 使用的 kubeadm 什么版本，决定你需要的镜像是什么
- 脚本执行完，会生成 k8s_images 目录
- k8s_images 目录保存的是你镜像的信息
- 执行 k8s_images下的load_image.sh 下的脚本，可以导入所有的镜像


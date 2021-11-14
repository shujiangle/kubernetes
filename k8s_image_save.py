#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import subprocess
import os


# get_image 是查看kubeadm所需镜像版本的函数
def get_image():
    get_image_list = subprocess.run("kubeadm config images list", stdout=subprocess.PIPE, shell=True)
    get_image_list = get_image_list.stdout.decode("utf8")
    print(get_image_list)
    print("\033[1;31m=" * 100, "\033[0m")


# save_image 是保存kubeadm所需镜像版本的函数
# k8s_images 目录保存镜像的所有信息
def save_image():
    if os.path.isdir("k8s_images"):
        print("\033[1;31m保存镜像目录 k8s_images已存在，无需创建\033[0m")
    else:
        print("\033[1;31m开始创建k8s_images目录\033[0m")
        os.mkdir("k8s_images")
        print("\033[1;31mk8s_images目录创建完成\033[0m")
    save_image_list = subprocess.run("kubeadm config images list", stdout=subprocess.PIPE, shell=True)
    save_image_list = save_image_list.stdout.decode("utf8")
    save_image_list_file = open("k8s_images/k8s_image.txt", "w")
    save_image_list_file.write(save_image_list)
    save_image_list_file.close()
    with open("k8s_images/k8s_image.txt", "r") as f:
        k8s_image_lists = f.readlines()
        k8s_image_lists = [image.strip() for image in k8s_image_lists]

    with open("k8s_images/load_image.sh", "w") as f:
        print("\033[1;31m正在创建导入镜像的shell脚本\033[0m")
        f.write("#!/bin/bash \n")
        f.write("ls *.tar|sort -h > ls.txt \n")
        f.write("for i in $(cat ls.txt) \n")
        f.write("do \n")
        f.write("    docker load < $i \n")
        f.write("done \n")
        f.write("rm -rf ls.txt \n")
        f.write('echo -e "\\e[1;31m 镜像导入完成 \\e[0m" \n')
        f.close()
        print("\033[1;31m导入镜像shell脚本创建完成，请查看k8s_images下的load_image.sh文件")
    for k8s_image_list in k8s_image_lists:
        subprocess.run(f"docker pull {k8s_image_list}", stdout=subprocess.PIPE, shell=True)
        images = k8s_image_list.split(":")[0].split("/")[-1]
        tag = k8s_image_list.split(":")[-1]
        subprocess.run(f"docker save -o k8s_images/{images}-{tag}.tar {k8s_image_list}", stdout=subprocess.PIPE,
                       shell=True)
    print("\033[1;31m镜像已经保存完成，请进入k8s_images目录查看")
    print("=" * 100, "\033[0m")


if __name__ == '__main__':
    print("\033[1;31m=" * 100, "\033[0m")
    print("\033[1;33m", " 1) 输入get_image，查看你的kubeadm 需要的镜像信息")
    print("  2) 输入save_image，拉取你需要的镜像", "\033[0m")
    print("\033[1;31m=" * 100, "\033[0m")
    print()
    print("\033[1;33m")

    # stty erase '^H' 使脚本执行过程中可以使用退格键退格
    subprocess.run("stty erase '^H'", stdout=subprocess.PIPE,
                   shell=True)
    inp = input("  请输入你的选择： ").strip()
    print("\033[0m")
    if inp == "get_image":
        get_image()
    elif inp == "save_image":
        save_image()
    else:
        print("你输入有问题，请重新输入： ")
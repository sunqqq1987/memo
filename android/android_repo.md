# repo的使用 #

    参考： https://blog.csdn.net/ican87/article/details/20726151

- 查看repo库上分支版本

        git --git-dir=.repo/manifests/.git/ branch -a

        或者：
        cd .repo/manifests
        git branch -a

- 获取当前的branch信息

        xxl@HP-Z228:~/aosp$ repo info
        Manifest branch: refs/tags/android-8.1.0_r2  //--当前的远程分支
        Manifest merge branch: refs/heads/android-8.1.0_r2
        Manifest groups: all,-notdefault
        ----------------------------
        Project: platform/art
        Mount path: /home/xxl/aosp/art
        Current revision: refs/tags/android-8.1.0_r2
        Local Branches: 0  //--没有对应的本地分支
        ----------------------------
        Project: platform/bionic
        Mount path: /home/xxl/aosp/bionic
        Current revision: refs/tags/android-8.1.0_r2
        Local Branches: 0
        ...

- 更换远程分支

        cd ~/aosp

        // repo init -u https://android.googlesource.com/platform/manifest -b android-8.1.0_r41
        => repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest -b android-8.1.0_r41 
           repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest -b android-wear-8.0.0_r1
           repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest -b android-wear-p-preview-2 

        repo sync -j8

- 查看本地的分支信息

        $repo branches
        如果显示 no branch , 则说明还没有任何分支
        xxl@HP-Z228:~/aosp$ repo branches
        (no branches)


- 创建本地分支

        repo start <new_branch> --all(或单个project) 
        相当于git checkout -b

- 切换到新分支

        repo checkout <new_branch> 
        相当于git checkout ，不带-b

- 安全删除不需要的分支

        repo prune <old_branch>


- 删除分支

        repo abandon

- 使用repo sync单独同步某个项目

        1)打开 .repo/manifiest.xml文件（这是隐藏文件夹，可用Ctrl+h显示）
        2)找到所要下载的project，使用path或者name字段的值都可以，直接跟在repo sync后作为参数即可

        比如：
        <project path="hardware/qcom/keymaster" name="platform/hardware/qcom/keymaster" groups="qcom,qcom_keymaster,pdk" />
        repo sync hardware/qcom/keymaster  //path部分的值就是project

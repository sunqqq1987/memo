# repo的使用 #

    参考： https://blog.csdn.net/ican87/article/details/20726151

    查看repo库上分支版本:
    git --git-dir=.repo/manifests/.git/ branch -a

    获取当前的branch:
        sam@ubuntu:~/aosp$ repo info
        Manifest branch: refs/tags/android-8.1.0_r2
        Manifest merge branch: refs/heads/android-8.1.0_r2
        Manifest groups: all,-notdefault
        ----------------------------
        Project: platform/art
        Mount path: /home/sam/aosp/art
        Current revision: refs/tags/android-8.1.0_r2
        Local Branches: 0

    查看分支状态：
    $repo branches
    如果显示 no branch , 则说明还没有任何分支

    创建分支：
    repo start <new_branch> --all(或project?)   
    相当于git checkout -b

    切换到新分支
    repo checkout <new_branch> 
    相当于git checkout ，不带-b

    安全删除不需要的分支 
    repo prune <old_branch>


    repo abandon
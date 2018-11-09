# GIT基本命令 #

**当对命令用法不熟悉的时候，可以使用**

    (1) –h选项: 显示简要用法说明 比如：git diff -h 
    (2) –help选项： 显示完整的用法说明 比如：git diff --help
 
## 常用git命令 ##

    1)只显示某个文件的提交
    git log --pretty=oneline 文件名

    2）显示某次提交
    git show <commit-id>
    git show <commit-id> --stat  //只显示修改的文件

    3)查看指定用户的git提交记录
    git log --author=username --pretty=oneline

    4)查找commit信息中的含指定信息的提交
    git log --grep=charger

    5)定制要显示的记录格式(时间)
    $ git log --pretty=format:"%h - %ae, %ar : %s" --grep=charger --author=codeaurora.org
    a68ce5d - 12@codeaurora.com, 3 months ago : drivers: usb: enable floated charger

    git log --pretty=format:"%h - %ae, %cd : %s" --grep=charger --author=xx.com
    ada5327 - bjzhu@xx.com, Fri Mar 30 04:24:14 2018 +0000 : Merge "drivers: usb: enable floated charger" into andr
    a68ce5d - bjzhu@xx.com, Fri Mar 30 12:00:02 2018 +0800 : drivers: usb: enable floated charger

    git log --pretty=format:"%h - %ae, %cd : %s" --grep=mobvoi.com

    //显示当前目录下的改动，包括改动的文件
    git log --pretty=format:"%h - %ae, %cd : %s" --grep=charger --author=xx.com --stat .

    参考：https://blog.csdn.net/c1958/article/details/76128056

    6) 基于远程分支创建本地分支
    git branch test1 remotes/xx
    git checkout test1

    如果想删除分支,则：
    git branch -d test1

    重命名本地分支:
    git branch -m old_local_branch_name new_local_branch_name

    7) 撤销本地分支的上一次commit
    git reset --hard HEAD^  //彻底回退工作区/暂存区/本地版本到当前版本库里的上一个版本（已经git commit到本地库）
    
    git reset HEAD  //当还没有commit时，回退index
    git reset HEAD^ //当有一次commit时，回退上次的commit和index

    8）更新远程分支的修改到当前分支

    方法1： <推荐>
    git fetch origin/xx //将远程库的修改更新到本地仓库
    git checkout my_branch  //切换到my_branch分支
    git merge origin/xx //将本地库的修改更新到当前的my_branch分支

    方法2：
    git pull 　　//这可能会发生merge

    方法3:
    先提交本地修改：git add, git commit
    再：
    git rebase   [other branch] //本地commit的修改会在最新的分支基础上，但可能会有冲突
    有冲突时:
    1)解决冲突
    2)git add 
    3)git rebase --continue, 无需执行 git commit. 


    9) git commit时修改作者信息
    git commit -m "xx"  --author="xx <xx@126.com>"
    注意author部分的格式
    

    10) 获得某个目录下的commit
    git log --pretty --stat . >~/xxl/study/charger/FG_commits.txt

    11) 打patch

    方法1: 
    https://blog.csdn.net/akb48fan710/article/details/73527767

    git apply 可以应用使用git diff 和git format-patch生成的2种patch来打补丁.
    使用git apply 命令之后patch文件中的修改会自动合入到对应的文件中,但是不会帮我们自动提交这个commit.

    方法2:
    https://blog.csdn.net/liuhaomatou/article/details/54410361

    git am 会直接使用patch文件中的diff的信息，还有提交者，时间等等来自动提交,不需要我们再去提交commit
    git am 必须使用的是用git format-patch 生成的patch文件来打补丁,而不能是使用git diff生成的patch.
    如果使用的是git diff生成的patch,会出现下面这个错误.
    Patch format detection failed.


    git am 可以一次合并一个文件，或者一个目录下所有的patch
    
    把生成的patch文件copy到一个文件夹中，然后:git am patch/*patch
    之后git log就看到有个commit了


    12）生成patch

    Git diff 和 git format-patch的对比.

    A.兼容性：很明显，git diff生成的Patch兼容性强。如果你在修改的代码的官方版本库不是Git管理的版本库，
    那么你必须使用git diff生成的patch才能让你的代码被项目的维护人接受。

    B.除错功能：对于git diff生成的patch，你可以用git apply --check 查看补丁是否能够干净顺利地应用到当前分支中；
    如果git format-patch 生成的补丁不能打到当前分支，git am会给出提示，并协助你完成打补丁工作，
    你也可以使用git am -3进行三方合并，详细的做法可以参考git手册或者《Progit》。从这一点上看，两者除错功能都很强。

    C.版本库信息：由于git format-patch生成的补丁中含有这个补丁开发者的名字，
    因此在应用补丁时，这个名字会被记录进版本库，显然，这样做是恰当的。因此，目前使用Git的开源社区往往建议大家使用format-patch生成补丁。


    把某次commit以后的（不包括该提交）都生成patch：
    git format-patch e795fefabc

    某次提交（包含）之前的几次提交，都生成patch：
    git format-patch –n 07fe  //n指patch数，07fe对应提交的名称
    git format-patch -1 07fe //只获取07fe提交的patch



    13)查看全部分支下的已经commit但没有push的:
    
    git log --branches --not --remotes

    14)commit msg后没有changeid
    网上下载commit-msg, 拷贝到 .git/hooks/commit-msg

    15) refs/for跟head的区别
    refs/for/[brach] 需要经过code review之后才可以提交，
    而refs/heads/[beanch]不需要code review。

 
## git diff ##

    (1) 三种比较方式
    $ git diff           #比较工作树与 暂存区
    $ git diff HEAD      #比较工作树与 当前分支中最后一次提交(HEAD)
    $ git diff --cached  #比较暂存区与 当前分支中最后一次提交(HEAD） 
    
     
    (2) 任意比较
    $ git diff test              #比较当前分支与 test分支
    $ git diff HEAD -- ./test    #比较当前分支最后一次提交与 工作树中的test文件 
    $ git diff HEAD^  HEAD       #比较当前分支的最后两次提交
     
    (3) 比较分支
    $ git diff topic master     #比较topic和master分支的HEAD, 所以也可以使本地分支和远程分支的比较
    $ git diff topic..master    #同1 
    $ git diff topic...master   #从topic分支开始时起, 在master分支上发生的更改
     
    (4) 限制输出格式
    $ git diff --diff-filter=MRC             #只显示修改、重命名和复制, 但不能添加或删除。 
    $ git diff --name-status                  #只显示名称和更改的性质, 而不是实际的 diff 输出。 
    $ git diff arch/i386 include/asm-i386     #将比较输出限制为子树 $ git diff –R 逆序输出差异
     
    (5) 查看当前分支中的两个commit id间的改动
    git diff commit-id-1 commit-id-2  >> diff.txt   #将2个commit间的不同 输出到文件 
    git diff commit-id-1 commit-id-2 -- readme.txt  #具体某个文件的commit间的变更
    
 
## git status /add/commit 提交修改到仓库 ##

**git status**  告诉我们工作区中哪些文件改动了（修改或删除了）。

    比如readme.txt被修改过了，但还没有提交。

    $ git status
    # On branch master
    # Changes not staged for commit:
    #   (use "git add <file>..." to update what will be committed)
    #   (use "git checkout -- <file>..." to discard changes in working directory)
    #
    #modified:   readme.txt
    no changes added to commit (use "git add" and/or "git commit -a")
 
**git add** 保存文件的修改到暂存区

    git add readme.txt      #添加文件的修改到暂存区
    git add –A               #添加工作区目录下所有文件的修改和删除，以及新增，添加到暂存区。
    git add –u                 #将工作区目录下所有文件的修改和删除(不包括新增的），添加到暂存区。

**git commit** 将修改提交到本地仓库

    $ git commit -m "append GPL"     #将暂存区的内容提交到本地版本库

    第一步是用git add把文件添加进去，实际上就是把文件修改添加到暂存区；
    第二步是用git commit提交更改，实际上就是把暂存区的所有内容提交到本地仓库的当前分支。
    如果要把两次修改合并后一块提交了，则可以：
    第一次修改 -> git add -> 第二次修改 -> git add -> git commit
    
    git commit -a –m ”Comments” 将所有被跟踪过的文件一次性提交到本地仓库，相当于git add + git commit -m

    git commit -s -m "modify file2" #单行注释

**添加多行注释的方法**

    git commit -s -m "module: submodule: title  #引号表示多行注释开始
    >
    >title
    >issue: XXX
    >
    >" #引号表示多行注释结束

**git commit --amend** 修改最后一次的提交

    一、如果已经push到远端服务器，想修改已经提交过的commit信息  
    1.保存:Ctrl + o; 回车 ;退出:Ctrl + x   
    # git commit --amend  

    2.重新提交gerrit审批  
    # git push --no-thin origin HEAD:refs/for/master  

    二、如果已经push到远端服务器,有漏掉的test.txt文件想提交到上一次的commit信息  
    1.添加test.txt  
    # git add test.txt

    2.修改commit信息;保存:Ctrl + o; 回车 ;退出:Ctrl + x   
    # git commit --amend 

    3.重新push到远端服务器  
    # git push --no-thin origin HEAD:refs/for/master 

## git log -> reflog -> reset 回退版本库的版本或暂存区的修改 ##

**git log** 只显示当前版本库里的所有提交记录的修改. 可以用来确定要回退到以前哪个版本。

    git log --pretty=oneline      #只简要地显示一行
    git log --stat                 #按commit显示每个commit所改动的文件
     
    git log -p -2 　#-p 选项展开显示每次提交的差异，-2 表示仅显示最近的两次提交的差异，否则显示所有提交的差异。
    git log –p --full-diff  #当指定路径，除路径外的文件的不同也显示出来

    git log -p --since="Tue Jul 25 21:15:04 2017 +0800" #获取指定日期后的提交

    git log -p --since=2.weeks : Check the info limited till 2 weeks before from current 

    git log remotes/origin/master     #查看远程库上的更改（要先fetch下来）
    git log --pretty=format:"%h %s" --graph  #按指定格式图形化显示提交记录

    git log --grep="search condition"  //查找commit message中满足指定条件的提交

**git reset** （前提是没有push到远程库）回退本地版本库的修改。
    
    git reset --hard HEAD  　//彻底回退工作区/暂存区/本地库的当前版本

    git reset               //撤消所有 git add（即撤销暂存区里的改动）
    git reset hello.c       //撤消所有 git add hello.c

    git reset --hard HEAD^  //彻底回退工作区/暂存区/本地库的上一个版本（用于已经commit到本地库的情况）
    HEAD表示当前版本，也就是最新的提交commit id:3628164...882e1e0，
    上一个版本就是HEAD^，上上一个版本就是HEAD^^，当然往上100个版本写100个^比较容易数不过来，所以写成HEAD~100。
    git reset --hard 3628164  //彻底回退工作区/暂存区/本地版本到指定的commit id

    git reset --mixed：此为默认方式(等价于git reset)，回退commit和index,但不回退工作区
    git reset HEAD //当git add后，但还没commit时，回退暂存区
    git reset HEAD^ //当有一次commit时，回退上次的commit和暂存区

    git reset --soft：回退到某个版本，只回退了commit，不回退工作区和index

 
**git reflog** 用来记录你的每一次命令, 以便确定要回到未来的哪个版本。
在回退到本地库的某个版本时特别有用

    $ git reflog
    ea34578 HEAD@{0}: reset: moving to HEAD^
    3628164 HEAD@{1}: commit: append GPL  //这里是最后的提交记录
    ea34578 HEAD@{2}: commit: add distributed
    cb926e7 HEAD@{3}: commit (initial): wrote a readme file
 
## git show ##

    git show <commit-id>  //只显示某个commit的改动
    
## git checkout ##

**撤销工作区的修改 git checkout -- < file >**

git checkout -- < file > #仅撤销工作区上的修改,使其回到索引区或本地仓库的状态

    事先用git status查看一下会被告知工作区的文件已经被改动：
    $ git status

    $ git checkout -- readme.txt // 回到最近一次git commit或git add后的状态
    命令git checkout -- readme.txt意思是把readme.txt文件在工作区的修改全部撤销，这里有两种情况：
    一种是readme.txt自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库的状态；
    一种是readme.txt已经添加到暂存区（git add）后，又作了修改，现在撤销修改就回到添加到暂存区后的状态。
    总之，就是让文件回到最近一次git commit或git add时的状态。
 
    场景2：当不但改乱了工作区某个文件第1行的内容，还把该文件第2行修改添加到了暂存区时，现在想丢弃暂存区的第2行修改，那么分两步：
    第一步用命令git reset HEAD file 使得文件成为unstage（即撤销掉了第2行修改），此时仅剩下了文件的最新修改（即第1行的修改)；
    第二步按场景1操作git checkout后撤销文件上的第1行修改。

**切换分支 git checkout < new_branch >**

git checkout < new_branch > 命令切换到新分支

**创建并切换分支 git checkout -b  < new_branch >**

    git checkout -b <new_branch> [<start_point>]
    参数-b <new_branch> 实现了创建分支和切换分支两个动作的合二为一
    相当于：
    git branch < new_branch >   创建新分支
    git checkout < new_branch >  切换到新分支

实例
    
    git checkout -- readme.txt  //丢弃工作区中readme.txt的修改（恢复为暂存区或本地仓库的版本）
    git checkout HEAD ./myfile
    git checkout <Branch name> -- <path> //checkout分支指定的文件，Get latest folder source for specific branch
    
    git checkout dev_branch   //切换到分支dev_branch且保留当前工作树的修改
    git checkout -b branch1   //创建新分支并切换到branch1
    git checkout -b branch1 origin/branch1 //Clone the project of remote storage and create in local storage
    git checkout -b mydev master //基于本地的master分支基础上创建新的本地分支mydev
    
    git checkout -b tmp-branch 0559ebf03c853938e4aa812b2b77bba73029c594 //基于指定的commit id进行checkout??
    
    
    git checkout -f [<branch>] 切换分支但会丢弃工作树和索引区的修改

## git rm ##

**删除暂存区、仓库和工作区上的文件: git rm -> commit**

    git rm file_path
    git commit -m 'delete somefile'

**删除暂存区、仓库上的文件, 但本地又需要使用:  git rm –cached  -> commit**

    git rm --cached file_path 
    git commit -m 'delete remote somefile'

## Github账户创建 ##

Github:  https://github.com

    本机上创建SSH Key，它会在个人目录下生成id_rsa和id_rsa.pub这两个文件。
    
    $ ssh-keygen -t rsa -C "your_email@example.com"
    最新：ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    然后将本机的ssh key添加到个人的github account setting 中。

## git remote ##
    
    git remote add <shortname> <url> //添加一个新的远程Git仓库，同时指定一个你可以轻松引用的简写shortname。
                如：git remote add origin git@github.com:samlin930/learngit.git
    
    git remote show [remote-name] //列出远程仓库的 URL 与跟踪分支的信息

## git push 将本地库到远程库 ##

    格式：git push [remote-name] [branch-name]//把本地的branch推送到远程库的branch

    git push -u origin master //把本地库的master分支推送到远程库的master

**对于本机来说，远程库的名字就是origin**，这是Git默认的叫法.
由于远程库是空的，我们第一次推送master分支时，加上了-u参数，Git不但会把本地的master分支内容推送的远程新的master分支，
还会把本地的master分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令:

    git push origin master

**将代码push到远程特定的分支上**

    格式：git push origin HEAD:refs/for/分支名

    代码提交到远程分支master上，则： 
    git push origin HEAD:refs/for/master  <src>:<dst>

**引用规格的格式**

    [remote "origin"]
        url = https://github.com/schacon/simplegit-progit
        fetch = +refs/heads/*:refs/remotes/origin/*
引用规格的格式由一个可选的 + 号和紧随其后的 <src>:<dst> 组成，其中 <src> 是一个模式（pattern），代表远程版本库中的引用；
<dst> 是那些远程引用在本地所对应的位置。 + 号告诉 Git 即使在不能快进的情况下也要（强制）更新引用。

默认情况下，引用规格由 git remote add 命令自动生成， Git 获取服务器中 refs/heads/ 下面的所有引用，并将它写入到本地的 refs/remotes/origin/ 中。 所以，如果服务器上有一个 master 分支，我们可以在**本地通过下面这种方式来访问该分支上的提交记录**：

    $ git log origin/master
    $ git log remotes/origin/master
    $ git log refs/remotes/origin/master

上面的三个命令作用相同，因为 Git 会把它们都扩展成 refs/remotes/origin/master。

**push时遇到的SSH错误**

    Bad configuration option: X11Forwrding 
    解决办法：注释或删除掉ssh config中的这行
 
删除之前和SSH关联的origin:
$ git remote rm origin
 
**查看当前项目远程分支的路径**

    git remote -v


## 查看远程库上的提交记录 ##

    git log remotes/origin/master

origin/master是默认的远程仓库和分支（但它是通过git fetch获取后放在本地的），可以自己改成想看的仓库和想看的分支
当然如果你的本地很久没有更新过远程仓库的信息了，看到的日志可能就不是最新的
所以在查看之前需要先运行:

    git fetch 或者git fetch origin

## git branch ##

    git branch -avv #查看本地所有的分支 
        v //显示每一个分支的最后一次提交
        * master //说明当前处于master分支

    如果想要查看设置的所有跟踪分支, 这会将所有的本地分支列出来并且包含更多的信息，
    如每一个分支正在跟踪哪个远程分支与本地分支是否是领先、落后或是都有。
    
    $ git branch -avv
      iss53     7e424c3 [origin/iss53: ahead 2] forgot the brackets
      master    1ae2a45 [origin/master] deploying index fix
    * serverfix f8674d9 [teamone/server-fix-good: ahead 3, behind 1] this should do it
      testing   5ea463a trying something new

    这里可以看到 iss53 分支正在跟踪 origin/iss53 并且 “ahead” 是 2，意味着本地有两个提交还没有推送到服务器上。 
    也能看到 master 分支正在跟踪 origin/master 分支并且是最新的。 
    接下来可以看到 serverfix 分支正在跟踪 teamone 服务器上的 server-fix-good 分支并且领先 2 落后 1，
    意味着服务器上有一次提交还没有合并入同时本地有三次提交还没有推送。 最后看到 testing 分支并没有跟踪任何远程分支。
    
    需要重点注意的一点是这些数字的值来自于你从每个服务器上最后一次抓取的数据。 
    如果想要统计最新的领先与落后数字，需要在运行此命令前抓取所有的远程仓库。 
    可以像这样做：$ git fetch --all; git branch -vv

    git branch -u origin/serverfix #设置已有的本地分支跟踪一个刚刚拉取下来的远程分支，或者想要修改正在跟踪的上游分支，
    你可以在任意时间使用 -u 或 --set-upstream-to 选项运行 git branch 来显式地设置。

    git branch  <new_branch>      #基于当前的分支（HEAD）创建新分支 
    git branch  -d <new_branch> #删除已经merge到当前分支的分支。 -D //强制删除
    git branch --merged         #查看哪些分支已经合并到当前分支
    git branch --no-merged         #查看所有包含未合并工作的分支

## git merge ##

### 无冲突的merge ###

    git merge origin #如果当前分支在master, 那么是将origin分支上的改动合并到master分支,
                        结果看起来就像一个新的"合并的提交"(merge commit)

    英文学习git merge guide:  https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
    merge advance: https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging

### 有冲突的merge ###

    $ git checkout master //切换到master分支 
    $ git merge issueFix //把issueFix中的内容Merge进来

如果没有冲突的话，merge完成。
有冲突的话，git会提示那个文件中有冲突，比如有如下冲突：

    <<<<<<< HEAD:test.c printf (“test1″); ======= printf (“test2″); >>>>>>> issueFix:test.c

    可以看到 ======= 隔开的上半部分是 HEAD中的内容，下半部分是在 issueFix 分支中的内容。

解决冲突的办法无非是二者选其一或者由你亲自整合到一起。

**(1)手动方式**

    比如你可以通过把这段内容替换为下面这样来解决：
    printf (“test2″);
    在解决了所有文件里的所有冲突后，运行 git add 将把它们标记为已解决（resolved）(因为一旦暂存，就表示冲突已经解决)。
    然后用 git commit 来完成这次合并提交。
 
**(2)图形界面方式**

运行 git mergetool，它会调用一个可视化的合并工具并引导你解决所有冲突：

    $ git mergetool
     
    merge tool candidates: kdiff3 tkdiff xxdiff meld gvimdiff opendiff emerge vimdiff
    退出合并工具以后，Git 会询问你合并是否成功。如果回答是，它会为你把相关文件暂存起来，以表明状态为已解决。
    然后用 git commit 来完成这次合并提交。

## git rebase ##

git rebase和git merge的区别：　https://www.cnblogs.com/pinefantasy/articles/6287147.html

### 原则 ###

    1）只对尚未推送或分享给别人的本地修改执行变基操作清理历史，从不对已推送至别处的提交执行变基操作。
    2）不要对在你的仓库外有副本的分支执行变基。

**将上游分支的改动串行地应用到当前分支： git rebase origin**

如果想让"mywork"分支看起来像没有经过任何合并一样，你可以用 git rebase:

    $ git checkout mywork
    $ git rebase origin //将上游分支origin的改动应用到mywork分支

    这些命令会把"mywork"分支里的每个提交(commit)取消掉，并且把它们临时保存为补丁(patch)(这些补丁放到".Git/rebase"目录中), 
    然后把"mywork"分支更新到最新的"origin"分支，最后把保存的这些补丁应用到"mywork"分支上。

**解决rebase过程中的冲突后执行： git rebase -- continue**

    在rebase的过程中，也许会出现冲突(conflict). 在这种情况，git会停止rebase并会让你去解决冲突.
    在解决冲突(可以用git mergetool或手动修改方式)后，用:
    git add 命令去更新这些内容的索引(index)
    然后只要执行: 
    git rebase --continue, 这样git会继续应用(apply)余下的补丁,无需执行 git commit. 
    。

**终止rebase： git rebase -- abort**

    用git rebase -- abort来终止rebase的行动，并且mywork分支会回到rebase开始前的状态。

**修改已经commit的message：  git rebase -i**

    首先要git rebase到需要修改message的那个commit的前1个commit。
    假设commit id是32e0a87f，运行下面的git rebase命令：

    git rebase -i 32e0a87f
    
    在git bash中运行上面的命令后，会弹出编辑框，在编辑框中会分行依次显示以pick开头的这个commit之后的所有commit message。
    将需要修改的commit message之前的"pick"改为"reword"，点击保存按钮，并关闭编辑框，这时会执行rebase操作。
    
    Rebasing (1/3)
    
    接着会再次弹出编辑框，这次编辑框中只有之前改为"reword"的那个commit message，此时修改commit message的内容，
    点击保存按钮并关闭编辑框，会继续执行rebase操作。 如果操作成功，会出现如下的提示：

    [detached HEAD aa3b52c] Add return url
     2 files changed, 1 insertion(+), 3 deletions(-)
    Successfully rebased and updated refs/heads/oss.

    这样就完成了git commit message的修改，然后强制push一下就搞定了：

    git push --force

**git rebase --onto** master server client

    以上命令的意思是：取出 client 分支，找出处于 client分支和 server分支的共同祖先之后的修改，
    然后把它们在 master 分支上重放一遍。

## git mergetool ##

    Use your confgured merge tool to solve conﬂicts
    用配置的mergetool来解决冲突
    
    $ git mergetool

## git cherry-pick ##

    格式：git cherry-pick <commit id>

git cherry-pick 可以将某一个分支中的一个或几个commit(s)来应用到当前分支。

例如，假设我们有个稳定版本的分支，叫v2.0，另外还有个开发版本的分支v3.0，
我们不能直接把两个分支合并，这样会导致稳定版本混乱，但是又想增加一个v3.0 中的功能到v2.0中，这里就可以使用cherry-pick了

    1 先在v3.0中查看要合并的commit的commit id
    git log 
    
    2 切到v2.0中, 假设是 commit f79b0b1ffe445cab6e531260743fa4e08fb4048b 
    git checkout  v2.0
    
    3 合并commit
    git cherry-pick f79b0b1ffe445cab6e531260743fa4e08fb4048b

如果发生冲突，会有如下提示：

    Automatic cherry-pick failed. After resolving the conflicts, 
    mark the corrected paths with 'git add <paths>' 
    or 'git rm <paths>' and commit the result with:  git commit -c 15a2b6c61927e5aed6718de89ad9dafba939a90b
     
**按普通方式解决并提交：**

    1 git status // 看哪些文件出现冲突 both modified: app/models/user.rb
    2 vim app/models/user.rb  //手动解决它。  
    3 git add app/models/user.rb 4 git commit -c  <新的commit号>
 
## 合并分支的代码 ##

假如有以下的情况：

    我本地和远程服务器各有一个代码仓库，本地的仓库有两个分支：master和simple分支，远程仓库也有两个分支：master和simple。
    两者一一对应。 现在我在master分支上添加了很多的内容，并提交到了服务器，现在想在simple分支上也加上同样的内容，怎么办呢？

### 方法有 ###

1）使用git merge命令

    git checkout simple 切换到simple分支 
    git merge master  将master分支合并到simple
 
2）使用git cherry-pick命令

    git checkout simple  切换到simple分支 
    git cherry-pick -n commit号 将某一次提交的内容合并过来 
    git cherry-pick ..master  将mster分支的整个提交内容都合并过来 
    git cherry-pick master
 
## git stash ##

    git stash //将新的储藏推送到栈上，运行 git stash 或 git stash save.  用于切换到其它分支工作前，保存未提交的修改
    git stash save -u "[my message]" //推荐。如果指定 --include-untracked 或 -u 标记，Git 也会储藏任何创建的未跟踪文件。 
                                        默认情况下，git stash 只会储藏已经在索引中的文件。
    git stash list //查看储藏的东西
    git stash apply //如果想要应用其中一个更旧的储藏，可以通过名字指定它，
                      像这样：git stash apply stash@{2}. 如果不指定一个储藏，Git 认为指定的是最近的储藏.
    git stash pop //要移除的储藏的名字来移除
    git stash clear //清空Git栈

    git stash show -p stash@{1}  //查看第二最近stash
    git stash show -p   //查看最近stash
     
    https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%82%A8%E8%97%8F%E4%B8%8E%E6%B8%85%E7%90%86#_git_stashing

## git tag ##

    git tag v1.4-lw  #创建轻量标签
    git tag -a v1.4 -m 'my version 1.4' #创建附注标签
    git tag -a v1.2 9fceb02              #后期打标签
    
    git checkout -b [branchname] [tagname] #在特定的标签上创建一个新分支

## git blame ##

    如果你在追踪代码中的一个 bug，并且想知道是什么时候以及为何会引入，文件标注通常是最好用的工具。 
    它展示了文件中每一行最后一次修改的提交。 所以，如果你在代码中看到一个有问题的方法，你可以使用 git blame 标注这个文件，
    查看这个方法每一行的最后修改时间以及是被谁修改的。 这个例子使用 -L 选项来限制输出范围在第12至22行：
    
    $ git blame -L 12,22 simplegit.rb

## git grep ##

    git grep –l [keyword]  //查找包括指定文件名关键字的提交
                           Regular use is possible in querying, searching file list which included keyword.
                           Refer https://git-scm.com/docs/git-grep for explanation regarding Git grep

## git init 建立仓库 ##

git init命令把当前目录变成Git可以管理的仓库：

    $ git init
    Initialized empty Git repository in /Users/michael/learngit/.git/


## Clone远程库到本地 ##

如果远程库已经准备好了，用命令git clone克隆一个本地库. 注意：该命令要在打算创建本地gitskill库的上一级目录上运行
 
    git clone git@github.com:samlin930/gitskills.git 
    Cloning into 'gitskills'... remote: Counting objects: 3, done. 
    
    $ cd gitskills $ ls README.md //可以看到文件已经获取到本地仓库了
 
**clone指定的分支**

    git clone -b <branch_name> <remote_repo>
    
# 其他 #

## git config ##

    config 配置有system级别 global（用户级别） 和local（当前仓库）三个 设置先从system-》global-》local  
    底层配置会覆盖顶层配置 分别使用--system/global/local 可以定位到配置文件

    查看系统config
    git config --system --list
    
    查看当前用户（global）配置    
    git config --global  --list
    
    查看当前仓库配置信息    
    git config --local  --list

## 设置代理 ##

    设置：
    git config --global http.proxy http://127.0.0.1:8087
    git config --global https.proxy https://127.0.0.1:8087
    
    #git config --global http.proxy 'socks5://127.0.0.1:8086/proxy.pac' 
    #git config --global https.proxy 'socks5://127.0.0.1:8086/proxy.pac'
    
    取消：
    git config --global --unset http.proxy
    git config --global --unset https.proxy

# 设置用户名和email #

    $ git config --global user.name ＂<user name>＂
    $ git config --global user.email ＂<mail address>“

## 提示SSL certificate problem ##

    git config --global http.sslVerify false

## 使用用户名/密码clone ##

    命令： git clone http(s)://username:password@remote
    
    例如：用户名 abc@qq.com, 密码是abc123456, git地址：git@xxx.com/www.git, 则：

    git clone http://abc@qq.com:abc123456@git.xxx.com/www.git


# repo 错误　＃

    1) repo sync error： cannot initialize work tree

    方法：
    先用 repo --trace sync -cdf 将repo的所有动作详细输出：
    : cd ......../vendor/mediatek/proprietary/hardware/gsm0710muxd
    : git read-tree --reset -u -v HEAD 1>| 2>|
    fatal: This operation must be run in a work tree

    再.repo/projects下以及.repo/project-objects/下　删除上述的.git目录，再repo sync即可

    参考：https://blog.csdn.net/ly890700/article/details/54848373

# 参考 #

    1）廖雪峰
    http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000

    2）wangjia55的专栏  http://blog.csdn.net/wangjia55/article/category/1334714

    3）git-scm 帮助   https://git-scm.com/docs

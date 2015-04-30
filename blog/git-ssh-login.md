#如何使用Git的SSH身份验证
## 生成秘钥
工具请随意，我用的是xshell，你也可以用ssh-keygen命令行，直接输入
>ssh-keygen

然后根据提示输入或者不输入一路回车也ok，然后会生成两个文件，一个是.pub是公钥，另一个是私钥

##在Git服务器上配置公钥
如果你用的是github，在用户设置->ssh中输入公钥，把生成的.pub文件中的内容复制进去就ok,最后需要输入密码

##本地配置
首先，如果你之前用https已经clone过了的话，要用git remote origin seturl git@github.com:xx/xx把协议改为ssh，否则即便配置成功ssh，push的时候还是要输入用户名密码

###Linux
如果你用的是linux，把私钥放到~/.ssh/目录下

> eval \`ssh-agent\`
>
> ssh-add ~/.ssh/id\_rsa\_2048
> 
> ssh -T git@github.com

看到成功提示。

###Windows
有点麻烦，机器一般都缺少环境变量HOME。

`ssh -T git@github.com` 的时候，默认去找private key的位置是`%HOME%/.ssh`, 所以需要设置环境变量 `set HOME=%USERPROFILE%`, `USERPROFILE`就是`C:\Users\username`这个目录，在其中 mkdir .ssh，再把key放进去就可以了.但是key的名字目前还是根据默认的去查找，所以要把private key改为id_rsa。目前还没找到能够自定义名称的方法，linux中倒是找到了，貌似是修改/etc/ssh/config可以对特定域名使用特定的key。windows搜索了一圈没有什么线索。

配置成功后，git push的时候就不用输入密码了。
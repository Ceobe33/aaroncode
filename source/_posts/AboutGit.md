---
title: About Git
date: "2022-10-01 17:41:08"
cover: AboutGit.png
tags:
    - Git
    - Note
description: Git operation && facing issue
---

## Issue

### Authentication

- -*generate ssh key**
  `$ ssh-keygen -t ed25519`

> authenticate cmd
> `$ ssh -T git@github.com`
Hi Coebe! You've successfully authenticated, -*but GitHub does not provide shell access**.

solve:  
  `$ git remote set-url origin git@github.com:Coebe/pragmadump.git`

- `connection refused`
  fix:
  1. check host
     `$ sudo vim /etc/hosts`
     add github.com ip hosts
     check github ip connection:
     `ssh -T -p 443 git@140.82.114.36`
  - `Failed to connect to raw.githubusercontent.com port 443 after 2 ms: Connection refused`
      fix:  
      1. add this config to host config file:`199.232.28.133 raw.githubusercontent.com`
  -   `fatal: unable to access 'https://github.com/EpicGames/UnrealEngine.git/': OpenSSL SSL_read: Connection was reset, errno 10054`
      1.  fix: `git config --global --add remote.origin.proxy ""`

### Command

- open local git config
  `$ git config --local -e`
- [same] -*Issue: not found repo**
  -`fatal: repository 'https://github.com/Coebe/aaroncode.git/' not found`*
- [same] -*Issue:**
  -`$ git pull`
  `fatal: unable to access 'https://github.com/Coebe/pragmadump.git/': OpenSSL SSL_connect: Connection was reset in connection to github.com:443`-
  - -*Fix:**
    `$ git remote set-url origin git@github.com:Coebe/aaroncode.git`

### Timeout

[Fixing git push/pull timing out](https://bengsfort.github.io/articles/fixing-git-push-pull-timeout/)  

- -*Issue:clone timeout**
  -`fatal: unable to access 'https://github.com/LunarVim/Neovim-from-scratch.git/': Failed to connect to github.com port 443 after 21057 ms: Timed out`*
  - -*Fix:**
    - look up the latest github.com ip address: [website](https://www.ipaddress.com/site/github.com)
    - add `000.000.000.000 github.com` append to `C:/Windows/System32/drivers/etc/hosts`
    - then complete
- -*Issue:pull timeout**
  -`$ git pull`  
  `ssh: connect to host github.com port 22: Connection timed out`  
  `fatal: Could not read from remote repository.`-
  - -*Fix:**
    - check permission when switch port
      `$ ssh -T -p 443 git@ssh.github.com`
    - succeed, then change ssh config file
      `vim ~/.ssh/config`
    - paste that save and exit
      `Host github.com`
      `Hostname ssh.github.com`
      `Port 443`
- -*Issue:push timeout**
  -`$ git push`  
  `fatal: unable to access 'https://github.com/Coebe/aaroncode.git/': Failed to connect to github.com port 443 after 21109 ms: Timed out`-
  - -*Fix:**
    - reset/add remote repo
    `$ git remote add origin https://github.com/username.git/`  
    other cmd  
    remove: `$ git remote remove <name>`
    - set push upstream  
    `$ git push --set-upstream origin main`
- -*Issue:** *`fatal: unable to access 'https://github.com/Coebe/aaroncode.git/': Failed to connect to 192.168.10.120 port 7890 after 21039 ms: Timed out`*
  - -*Fix:**
- -*Issue:**
  -`$ git clone`  
  `fatal: unable to access 'https://github.com/ThePrimeagen/vim-be-good.git/': Failed to connect to 192.168.10.120 port 7890 after 21080 ms: Timed out`-
  - -*Fix:**
    - proxy problem clear that all be fine  
     `git config --global --unset http.xxx`  
    - if wanna set proxy:
     `git config --global http.proxy http://xxx/`
      if needs account & password -*don't know meaning**  
      `git config --global http.proxy http://user:pwd@ipaddress:port`

### Secure & Authentication

- -*Issue: ssl**
  `fatal: unable to access 'https://github.com/Coebe/aaroncode.git/': OpenSSL SSL_read: Connection was reset, errno 10054`
- -*Fix:**
  `$ git config --global http.sslVerify "false"`
- Add SSH Key over GitHub
  -Key is invalid. You must supply a key in OpenSSH public key format*
  - do not use PRIVATE key, use the `.pub` sub file (under directory: ~/.ssh/)

### Submodule



![Submodule](https://s2.loli.net/2022/11/02/iRJrgEc4mDWOPUT.png)this image mean has `.git` file in child directory, 然后GitHub就会把这个文件夹视为一个子系统模块,从而不能正常更新Git  

solve step:

1. delete child directory `.git` file.
2. execute `git rm --cached [filename] // filename is the submodule directory`.
3. execute `git add .`.
4. execute `git commit`.
5. execute `git push origin [branchName]`.

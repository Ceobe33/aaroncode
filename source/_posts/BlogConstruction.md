---
title: The Step of Blog Construction
date: "2022-10-10 17:40:08"
cover: BlogConstruction.png
description: Hexo blog facing issue
---

### Reference

[![Netlify Status](https://api.netlify.com/api/v1/badges/6417f999-72a6-4ebd-994d-0d5118d42bb3/deploy-status)](https://app.netlify.com/sites/sprightly-croquembouche-951681/deploys)  

### Using Blog

修改根配置文件的这个参数，：使用资源文件的文件展示
over config file change `post_asset_floder: true` parameter, then can use local path to config cover (maybe all the photo/img?)

[official document](https://hexo.io/zh-cn/docs/writing.html)  
generate new blog file:
`hexo new <filename>`

#### Blog Beauty

- cardInfo hover anim path

  `themes\butterfly\source\css\_layout\aside.styl:55`

#### Scroll Bar

1. create css file
   my path: `aaroncode\source\custom\scrollBar.css`
2. using that css in `config.inject`

   ```yml
   <!-- _config.yml -->
   <!-- context -->
   ...
   inject:
     head:
       - <link rel="stylesheet" href="/custom/scrollBar.css">
     bottom:
       # - <script src="xxxx"></script>
   ...
   <!-- context -->
   ```

3. modified css file to beauty scroll bar

   ```css
   <!-- my config -->
    /* 滚动条 */
   
    /* no effect about width setting */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
   
    ::-webkit-scrollbar-track {
        background-color: rgba(160, 217, 255, 0.623);
        /* border-radius: 100em; */
    }
   
    /* the bar */
    ::-webkit-scrollbar-thumb {
        background-color: rgb(248, 156, 156);
        background-image: -webkit-linear-gradient(45deg,
                /* render sequence is reverse */
                rgb(255, 149, 149) 10%,
   
                rgb(155, 243, 255) 30%,
                rgb(158, 156, 248) 50%,
                rgb(155, 243, 255) 75%,
   
                transparent 85%,
                transparent);
        border-radius: 5em;
    }
   
    ::-webkit-scrollbar-corner {
        background-color: transparent;
    }
   
    /* ::-moz-selection {
        color: #fff;
        background-color: #00eeff;
    } */
   ```

### Issuse

### Aout post

在使用博客资源展示图片时如果使用github的路径为什么需要在链接末尾加上`?raw=true` ?

### About Connexity ~连通性问题~

bug statement:  
打开网站`HTTP ERROR 502`  

solution:  
原因是访问不到Hexo所指的服务, 也就是代理出现了问题, 查看Cloudflare DNS配置,并修改成 CNAME 模式(通过 Cloudflare 转发 [aaroncode].netlify.app)

#### About Cache ~缓存问题~

bug statement:  
> extends includes/layout.pug block content include ./includes/mixins/post-ui.pug #recent-posts.recent-posts +postUI include includes/pagination.pug

solution:  

1. 在hexo根目录执行命令：
`npm install --save hexo-renderer-jade hexo-generator-feed hexo-generator-sitemap hexo-browsersync hexo-generator-archive`  
2. 清除缓存
`hexo clean`  
3. 重新生成静态文件
`hexo g`/`hexo generate`

```C++
code block example
```

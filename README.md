# disflash
disflash —— 关掉 flash 计划

## 介绍
disflash 计划是希望在关掉 flash 或者浏览器默认不再提供 flash 的时候还能浏览国内的视频网站的视频。

*暂时只在 Chrome 里测试过。*

目前已支持：

* 优酷
* 腾讯视频
* Bilibili 直播
* AcFun
* 音悦台

## 使用

**需要 Python 3 。**

### ① 安装依赖
```
pip3 install -r backend/requirements.txt
```

### ② 安装 Tampermonkey 脚本

打开 Chrome ，安装 Tampermonkey 插件。在 Tampermonkey 里新建插件，
把 [monkey_script.js](https://github.com/sljeff/disflash/blob/master/monkey_script.js) 的内容复制到代码框里，保存即可。

### ③ 运行 server
```
python3 backend/main.py
```

### ④ 然后打开已支持的视频网站看看效果吧。

## 如何给 disflash 编写扩展
-----------------------
待完成。
-----------------------

## 另

做 disflash 的想法是来源于 [MAMA2](https://github.com/zythum/mama2) 。
> 为什么不用 MAMA2 或者给 MAMA2 写扩展?

> ① MAMA2 已经有些时间没更新了，部分网站已经失效。
一些失效的原因，比如搜狐视频和优酷，其实不是视频地址爬取失败了，而是返回 HTTP 头的 `Access-Control-Allow-Origin` 没有包含 PC 页面，
浏览器安全机制拒绝了它。
还有一些是另外的安全机制，比如复杂请求前给跨域的地址发送 OPTION 请求，会被视频源拒绝。这需要一个运行的 server 来做
（如果 MAMA2 没有缺省解析服务的话，是需要跑一个 server 的，而这个 server 只用来返回播放器和播放地址，功能比较受限）。

> ② 一些网站比如音悦台/腾讯视频的 PC 版已经自带 HTML5 播放器了，而且音悦台只需要一个跳转即可。
不过腾讯视频需要在视频的部分载入前让浏览器的 UA 是 Mac 的 safari，这也是 MAMA2 做不到的（因为 MAMA2 就是给 Mac 用户用的……）。

> ③ node 平台的各种包依赖问题让编写 MAMA2 变得很难受……

所以 disflash 需要前后端共同配合来得到视频内容。对于比较严谨的网站（比如视频地址的`Access-Control-Allow-Origin`不是`*`的……），
浏览器端执行网页里的 JS ，并且加入 Tampermonkey 脚本用来做一些受浏览器限制的事；
服务端通过代理的方法可以模拟手机端以及解决跨域的问题。

disflash 有一个 tornado 的简单 server ，而复杂的逻辑都交给规则（backend 里的 rules 文件夹）。
这些规则是 Python 文件，所以它可以做任何事情。

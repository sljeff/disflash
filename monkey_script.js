// ==UserScript==
// @name         disflash——取代 flash 计划
// @namespace    https://www.kindjeff.com/
// @version      2017.2.21
// @description  disflash 计划：https://github.com/sljeff/disflash
// @author       kindJeff
// @match        http://v.youku.com/v_show/*
// @match        http://live.bilibili.com/*
// @match        https://live.bilibili.com/*
// @match        http://*.acfun.cn/*
// @include      *://v.qq.com/*
// @include      *://lol.qq.com/v/*
// @include      *://film.qq.com/*
// @include      *://view.inews.qq.com/*
// @require      https://localhost:9527/util/get_flvjs/
// run-at        document-start
// @grant        none
// ==/UserScript==

if(location.href.indexOf('.qq.com/')!==-1){
    Object.defineProperty(navigator, 'plugins', {
      get: function () {
        return { length: 0 };
      }
    });
    Object.defineProperty(navigator,"userAgent",{
        value:"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10;  rv:48.0) Gecko/20100101 Firefox/48.0",
        writable:false,
        configurable:false,
        enumerable:true
    });
}

else if(location.href.indexOf('.acfun.cn')!==-1){
    //noinspection JSAnnotator
    document.domain = 'acfun.cn';
}

else{
    setTimeout(function(){
        s=document.body.appendChild(document.createElement('script'));
        s.src='https://localhost:9527/getscript/' + location.href;
    }, 2000);
}
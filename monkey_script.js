// ==UserScript==
// @name         disflash——取代 flash 计划
// @namespace    https://www.kindjeff.com/
// @version      2017.2.20
// @description  disflash 计划：https://github.com/sljeff/disflash
// @author       kindJeff
// @match        http://v.youku.com/v_show/*
// @require      https://localhost:9527/util/get_flvjs/
// @require      https://localhost:9527/util/get_hlsjs/
// run-at        document-start
// @grant        none
// ==/UserScript==

if(location.href.indexOf('v.youku.com')!==-1){
    setTimeout(function(){
        s=document.body.appendChild(document.createElement('script'));
        s.src='https://localhost:9527/getscript/' + location.href;
    }, 3000);
}
else if(null){
    // other
}
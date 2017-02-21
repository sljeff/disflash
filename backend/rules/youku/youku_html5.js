/**********************/
/*get info from iframe*/
/**********************/
var YKP_userCache;
function add_iframe () {
    var page_name = location.pathname.split('/')[2];
    var m_url = 'http://m.youku.com/video/' + page_name;
    var m_iframe = document.createElement('iframe');
    m_iframe.id = 'mobile_iframe';
    m_iframe.setAttribute('name', 'mobile_iframe');
    m_iframe.src = m_url;
    document.body.appendChild(m_iframe);
    m_iframe.onload = function () {
        YKP_userCache = document.mobile_iframe.YKP.userCache;
        m_iframe.remove();
        init_and_start();
    }
}

add_iframe();


/**********************/
/*  get video source  */
/**********************/
function translate(a, b) {
    for (var c = [], d = 0; d < a.length; d++) {
        var e = 0;
        e = a[d] >= "a" && a[d] <= "z" ? a[d].charCodeAt(0) - "a".charCodeAt(0) : a[d] - "0" + 26;
        for (var f = 0; f < 36; f++)
            if (b[f] == e) {
                e = f;
                break
            }
        e > 25 ? c[d] = e - 26 : c[d] = String.fromCharCode(e + 97)
    }
    return c.join("")
}

function rc4(a, b) {
    for (var c, d = [], e = 0, f = "", g = 0; g < 256; g++)
        d[g] = g;
    for (g = 0; g < 256; g++)
        e = (e + d[g] + a.charCodeAt(g % a.length)) % 256,
        c = d[g],
        d[g] = d[e],
        d[e] = c;
    g = 0,
        e = 0;
    for (var h = 0; h < b.length; h++)
        g = (g + 1) % 256,
        e = (e + d[g]) % 256,
        c = d[g],
        d[g] = d[e],
        d[e] = c,
        f += String.fromCharCode(b.charCodeAt(h) ^ d[(d[g] + d[e]) % 256]);
    return f
}

function encode64 (a) {
    if (!a)
        return "";
    a = a.toString();
    var b, c, d, e, f, g, h = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    for (d = a.length,
        c = 0,
        b = ""; c < d;) {
        if (e = 255 & a.charCodeAt(c++),
            c == d) {
            b += h.charAt(e >> 2),
                b += h.charAt((3 & e) << 4),
                b += "==";
            break
        }
        if (f = a.charCodeAt(c++),
            c == d) {
            b += h.charAt(e >> 2),
                b += h.charAt((3 & e) << 4 | (240 & f) >> 4),
                b += h.charAt((15 & f) << 2),
                b += "=";
            break
        }
        g = a.charCodeAt(c++),
            b += h.charAt(e >> 2),
            b += h.charAt((3 & e) << 4 | (240 & f) >> 4),
            b += h.charAt((15 & f) << 2 | (192 & g) >> 6),
            b += h.charAt(63 & g)
    }
    return b
}

function xhr_with_callback(url, callback, xheader, method){
    if(method===undefined)
        method = 'GET';

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(xhr.readyState==4 && xhr.status==200){
            callback(xhr.responseText);
        }
    };
    xhr.open(method, url);
    for(var name in xheader) {
        xhr.setRequestHeader(name, xheader[name]);
    }
    xhr.send();
}

var proxy_root = 'https://localhost:9527';
var get_stream_url= proxy_root+'/proxy/http://play-ali.youku.com/play/get.json?vid='+location.href.match(/id_.*html/)[0].slice(3,-5)+'&ct=10';
var get_ip_url = proxy_root+'/util/get_ip/';
var flvjs_url = proxy_root+'/util/get_flvjs/';
var stream_data, my_ip;

function init_and_start(){
    xhr_with_callback(get_ip_url, function(resText){
        var data = JSON.parse(resText.toString());
        var ip_arr = data.ip.split('.');
        var result = '';
        for (var i of ip_arr) {
            result += ("000000000"+parseInt(i, 10).toString(2)).slice(-8);
        }
        my_ip = parseInt(result, 2);

        xhr_with_callback(get_stream_url, function(resText){
            var data = JSON.parse(resText.toString());
            stream_data = data.data;
            //xhr_with_callback(flvjs_url, function(resText){
                //eval(resText);
                add_video_into_arr();
            //});
        }, {'X-Cookie': document.cookie});
    });
}

function getVideoSrc(index_of_stream, index_of_segs, stream_data, stream_type, file_id, f, g) {
    var h = stream_data.stream[index_of_stream];
    var i = stream_data.video.encodeid;
    if(!i || !stream_type)
        return;
    var j = {
            flv: 0,
            flvhd: 0,
            mp4hd: 1,
            mp4hd2: 2,
            mp4hd3: 3,
            "3gphd": 0,
            "3gp": 0
        },
        k = j[stream_type],
        l = {
            flv: "flv",
            mp4hd: "mp4",
            mp4hd2: "flv",
            mp4hd3: "flv",
            "3gphd": "mp4",
            "3gp": "flv",
            flvhd: "flv"
        },
        m = l[stream_type],
        n = index_of_segs.toString(16);
    1 == n.length && (n = "0" + n);
    var o = h.segs[index_of_segs].total_milliseconds_video / 1e3;
    var a4 = 'boa4', e = file_id, p = h.segs[index_of_segs].key;
    "" != p && p != -1 || (p = h.key2 + h.key1);
    var q = "";
    stream_data.show && (q = stream_data.show.pay ? "&ypremium=1" : "&ymovie=1");
    var r = "/player/getFlvPath/sid/" + YKP_userCache.sid + "_" + n + "/st/" + m + "/fileid/" + e + "?K=" + p + "&hd=" + k + "&myp=0&ts=" + o + "&ypp=0" + q;

    var s = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26];
    var t = encodeURIComponent(encode64(rc4(translate(a4 + 'poz' + YKP_userCache.a2, s).toString(), YKP_userCache.sid + "_" + e + "_" + YKP_userCache.token)))
    r += "&ep=" + t;
    r += "&ctype=12";
    r += "&ev=1";
    r += "&token=" + YKP_userCache.token;
    r += "&oip=" + my_ip;
    r += (f ? "/password/" + f : "") + (g ? g : "");
    r = "//k.youku.com" + r;
    return r;
}


var video_arr = [];

function add_video_into_arr () {
    for(var stream_index in stream_data.stream){
        var one_stream = stream_data.stream[stream_index];
        var segs = one_stream.segs;

        var a_type_of_video = {}
        a_type_of_video.size = one_stream.size;
        a_type_of_video.audio_lang = one_stream.audio_lang;
        a_type_of_video.ms_v = one_stream.milliseconds_video;
        a_type_of_video.ms_a = one_stream.milliseconds_audio;
        a_type_of_video.width = one_stream.width;
        a_type_of_video.height = one_stream.height;
        a_type_of_video.protocol = one_stream.transfer_mode;
        a_type_of_video.stream_type = one_stream.stream_type;
        a_type_of_video.is_flv = segs[0].path.indexOf('/flv/')!==-1?true:false;
        a_type_of_video.segments = []
        for(var seg_index in segs){
            var one_seg = segs[seg_index];
            var one_video = {};
            one_video.duration = parseInt(one_seg.total_milliseconds_video);
            one_video.filesize = parseInt(one_seg.size);
            var real_url = getVideoSrc(stream_index, seg_index, stream_data, one_stream.stream_type, one_seg.fileid);
            one_video.url = proxy_root+'/proxy/http:' + real_url;
            a_type_of_video.segments.push(one_video);
        }
        video_arr.push(a_type_of_video);
    }
    set_video();
}



/**********************/
/*   set video area   */
/**********************/
function set_video () {
    var btn_div = document.createElement('div');
    var video_div = document.createElement('div');
    var video_dom = document.createElement('video');
    var player = document.getElementById('player');
    btn_div.style.textAlign = 'center';
    video_div.textAlign = 'center';
    video_dom.id = 'modal_player';
    video_dom.setAttribute('controls', 'controls');
    video_dom.setAttribute('autoplay', 'autoplay');
    document.querySelector('div.base_info').appendChild(btn_div);
    document.getElementById('vpactionv5_wrap').remove();
    video_div.appendChild(video_dom);
    video_dom.style.width = player.clientWidth + 'px';
    video_dom.style.height = player.clientHeight + 'px';

    player.children[0].remove();
    player.appendChild(video_div);

    for(var video_index in video_arr){
        var stream_type = video_arr[video_index].stream_type;
        if(stream_type == 'mp4hd')
            continue;
        var btn_title;
        switch(stream_type){
            case 'flvhd':
                btn_title='高糊'; break;
            case 'mp4hd2':
                btn_title='高清'; break;
            case 'mp4hd3':
                btn_title='超清'; break;
        }
        var btn = document.createElement('button');
        btn.textContent = btn_title;
        btn.id = 'btn-' + video_index;
        btn.className = 'video-btn';
        btn.style.marginLeft = '10px';
        btn_div.appendChild(btn);
    }

    for(var btn of document.getElementsByClassName('video-btn')){
        btn.onclick = function(){
            if(window.currentPlayer!==undefined)
                window.currentPlayer.destroy();
            var this_id = this.id;
            var video_index = parseInt(this_id.slice(this_id.indexOf('-')+1));
            var current_stream = video_arr[video_index];
            if (flvjs.isSupported()) {
                var videoElement = video_dom;
                window.currentPlayer = flvjs.createPlayer({
                    type: current_stream.is_flv?'flv':'mp4',
                    filesize: parseInt(current_stream.size),
                    duration: parseInt(current_stream.ms_v),
                    segments: current_stream.segments
                });
                currentPlayer.attachMediaElement(videoElement);
                currentPlayer.load();
                currentPlayer.play();
            }
        };
    }
}
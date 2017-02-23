var api_link = 'http://m.tv.sohu.com/phone_playinfo?';
var params = {
    vid: vid,
    site: 1,
    appid: 'tv',
    api_key: 'f351515304020cad28c92f70f002261c',
    plat: 17,
    sver: 1.0,
    partner: 1,
    uid: (new Date()).getTime() * 1000,
    muid: (new Date()).getTime() * 1000,
    _c: 1,
    pt: 3,
    qd: 680,
    src: 11050001,
    _: (new Date()).getTime()
};
var url = api_link + $.param(params);

var proxy_root = 'https://localhost:9527';
$.getScript(proxy_root + '/util/get_hlsjs/', function() {
    get_info_and_add_video();
});

function get_info_and_add_video(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://localhost:9527/proxy/' + url);
    xhr.onreadystatechange = function () {
        if(xhr.readyState===4 && xhr.status===200){
            add_video(xhr.responseText);
        }
    }
    xhr.send();
}

function add_video(data) {
    var video_data = JSON.parse(data).data;
    var w = $("#player").width();
    var h = $("#player").height();
    var h5_player = document.createElement('video');
    $(h5_player).width(w);
    $(h5_player).height(h);
    $("#player").replaceWith(h5_player);
    h5_player.setAttribute('controls', 'controls');
    h5_player.setAttribute('autoplay', 'true');
    $('#phone-download').children().remove();
    var video_urls = {
        'blue': video_data.url_blue,
        'super': video_data.urls.m3u8.sup[0],
        'high': video_data.urls.m3u8.hig[0],
        'low': video_data.urls.m3u8.nor[0]
    };
    for (var index in video_urls) {
        if (video_urls[index] !== undefined) {
            var url = proxy_root + '/proxy/' + video_urls[index];
            var btn = document.createElement('button');
            btn.textContent = index;
            btn.className = 'ctl_btn';
            btn.setAttribute('df-index', index);
            btn.setAttribute('df-url', url);
            $(btn).appendTo('#phone-download');
        }
    }
    $('.ctl_btn').on('click', function() {
        if (Hls.isSupported()) {
            if (window.video_hls !== undefined) {
                window.video_hls.detachMedia();
                window.video_hls.destroy();
            }
            window.video_hls = new Hls();
            video_hls.loadSource($(this).attr('df-url'));
            video_hls.config.xhrSetup = function(xhr, url){
                xhr.setRequestHeader('X-Cookie', document.cookie);
            }
            video_hls.attachMedia(h5_player);
            video_hls.on(Hls.Events.MANIFEST_PARSED, function() {
                video.play();
            });
        }
    });
}
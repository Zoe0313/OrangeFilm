window.onload = function(){
    //登录状态
    var header_body = '';
    var nickname = window.localStorage.getItem('dnblog_nickname')
    if (nickname){
        header_body += '<a href="javascript:loginOut()">'+ nickname +' 注销</a>';
    }else{
        header_body += '<a href="/login">登录/注册</a>';
    }
    var userinfo = $("#userinfo");
    userinfo.html(header_body);
};

function loginOut(){
    if(confirm("确定登出吗？")){
        window.localStorage.removeItem('dnblog_token');
        window.localStorage.removeItem('dnblog_email');
        window.localStorage.removeItem('dnblog_nickname');
        window.location.href= '/';
    }
}

function onSearch(){
    var search_word = $('input')[0].value;
    console.log("onSearch: ",search_word);
    if (search_word) {
        window.location.href = '/film/search?key=' + search_word;
    }
}

function showSearchList(search_word){
    //var get_url = "http://127.0.0.1:8000/v1/films/search" + "?" + 'key=' + search_word;
    var get_url = "http://139.155.144.42:8000/v1/films/search" + "?" + 'key=' + search_word;
    $.ajax({
        type:"get",
        url: get_url,
        success:function (result) {
            if (200 == result.code){
                var films = result.data.films;
                var total = result.data.total;
                setupSearchList(films);
            }else{
                alert(result.error)
            }
        }
    });
}


function setupSearchList(films){
    var filmSize = films.length;
    var html_body = ""
    if(filmSize == 0){
        html_body += '<h1>空空如也</h1>';
    } else {
        for (var t=0; t<filmSize; t++) {
            var detail_url = 'https://maoyan.com' + films[t].detail_url;
            var img_url = '/static/images/movies/'+films[t].img_url;
            var name = films[t].name;
            var ntype = films[t].type;
            var duration = films[t].duration;
            var release_time = films[t].release_time;
            var score = films[t].score;
            var directors = films[t].directors;
            var actors = films[t].actors;
            var introduce = films[t].introduce;

            html_body += '<div class="item" data-scroll-reveal="enter bottom over 1s">';
            html_body += '<div class="gname">';
            html_body += '<a href="' + detail_url + '"><img src="' + img_url + '"></a>';
            html_body += '<a href="' + detail_url + '"><p>' + name + '</p></a>';
            if (ntype=='later') {
                html_body += '<p>' + score + ' 人想看</p>';
            }else{
                html_body += '<p>评分：' + score + '</p>';
            }
            html_body += '<p>时长：' + duration + '</p>';
            html_body += '<p>' + release_time + '</p>';
            html_body += '</div>';

            html_body += '<div class="ginfo">';
            html_body += '<p>' + directors + '</p>';
            html_body += '<p>' + actors + '</p>';
            html_body += '<p>' + introduce + '</p>';
            html_body += '</div>';

            html_body += '</div>';
        }
    }
    $(".content").html(html_body);
}
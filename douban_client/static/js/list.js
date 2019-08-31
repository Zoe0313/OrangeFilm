function showFilmList(ntype, npage){
    //var get_url = "http://127.0.0.1:8000/v1/films/" + ntype + "/" + npage;
    var get_url = "http://139.155.144.42:8000/v1/films/" + ntype + "/" + npage;
    $.ajax({
        // 请求方式
        type:"get",
        // url
        url: get_url,
        success:function (result) {
            if (200 == result.code){
                var films = result.data.films;
                var total = result.data.total;
                setupList(films,ntype);
                refreshPage(ntype,npage,total);
            }else{
                alert(result.error)
            }
        }
    });
}

function setupList(films,ntype){
    var filmSize = films.length;
    var html_body = ""
    if(filmSize == 0){
        html_body += '<h1>空空如也</h1>';
    } else {
        for (var t=0; t<filmSize; t++) {
            var detail_url = 'https://maoyan.com' + films[t].detail_url;
            var img_url = '/static/images/movies/'+films[t].img_url;
            var name = films[t].name;
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
            if (ntype==2) {
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

function refreshPage(ntype,npage,total) {
    var html_body = '<br>';
    var pageSize = Math.floor(total/10);
    if (total%10>0) {
        pageSize++;
    }

    if (npage>0) {
        var prev_page = npage-1;
        html_body += '<a href="/film/' + ntype + '/' + prev_page + '"><</a>';
    }
    for (var i=0; i<pageSize; i++) {
        var show_page = i+1;
        if (npage==i) {
            html_body += '<strong class="select"><u>' + show_page + '</u></strong>';
        }else{
            html_body += '<a href="/film/' + ntype + '/' + i + '">' + show_page + '</a>';
        }
    }
    if (npage+1<pageSize) {
        var next_page = npage+1;
        html_body += '<a href="/film/' + ntype + '/' + next_page + '">></a>';
    }
    $(".page").html(html_body);
}
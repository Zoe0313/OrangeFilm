function getFilmsByType(ntype,selectorName) {
    //var get_url = "http://127.0.0.1:8000/v1/films/" + ntype + "/0";
    var get_url = "http://139.155.144.42:8000/v1/films/" + ntype + "/0";
    $.ajax({
        type:"get",
        url: get_url,
        success:function (result) {
            if (200 == result.code){
                var films = result.data.films;
                var html_body = setupList(films,ntype);
                var films = $(selectorName);
                films.html(html_body);
            }else{
                alert(result.error);
            }
        }
    });
}

function setupList(films,ntype) {
    var t = 0;
    var filmSize = films.length;
    var html_body = '';
    for (var row=0; row<2; row++) {
        html_body += '<div class="line">';
        for (var col=0; col<5; col++) {
            var detail_url = 'https://maoyan.com' + films[t].detail_url;
            var img_url = '/static/images/movies/'+films[t].img_url;
            //console.log(img_url);
            var name = films[t].name;
            var score = films[t].score;
            html_body += '<div class="item">';
            html_body += '<a href="' + detail_url + '"><img src="' + img_url + '" width="140px" height="196px"></a>';
            html_body += '<a href="' + detail_url + '"><p>' + name + '</p></a>';

            if (ntype==2) {
                html_body += '<p>' + score + ' 人想看</p>';
            }else{
                html_body += '<p>评分：' + score + '</p>';
            }
            html_body += '</div>';
            t++;

            if (t>=filmSize) {
                break;
            }
        }
        html_body += '</div>';
        if (t>=filmSize) {
            break;
        }
    }
    return html_body;
}
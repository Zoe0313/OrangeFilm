function register(){
    var email = $('.signIn-email').val()
    var nickname = $('.signIn-nickname').val()
    var password = $('.signIn-password').val()
    var post_data = {'email':email, 'nickname':nickname, 'password':password }

    $.ajax({
        // 请求方式
        type:"post",
        // contentType
        contentType:"application/json",
        // dataType
        dataType:"json",
        // url
        //url:"http://127.0.0.1:8000/v1/users",
        url:"http://139.155.144.42:8000/v1/users",
        // 把JS的对象或数组序列化一个json 字符串
        data:JSON.stringify(post_data),
        // result 为请求的返回结果对象
        success:function (result) {
            if (200 == result.code){
                window.localStorage.setItem('dnblog_token', result.data.token)
                window.localStorage.setItem('dnblog_nickname', result.nickname)
                window.localStorage.setItem('dnblog_email', result.email)
                alert('注册成功')
                //取本会话的上一跳
                refer_url = document.referrer

                //如果是项目内部的请求，回跳到上一步
                if (refer_url.search('127.0.0.1') != -1){
                    window.location = refer_url;
                    console.log('refer_url=',refer_url)
                }else{
                    window.location =  '/';
                    console.log('/')
                }
            }else{
                alert(result.error)
            }
        }
    });
}

function login(){
    var email = $('.signIn-email').val()
    var password = $('.signIn-password').val()
    var post_data = {'email':email, 'password':password }

    $.ajax({
        // 请求方式
        type:"post",
        // contentType
        contentType:"application/json",
        // dataType
        dataType:"json",
        // url
        //url:"http://127.0.0.1:8000/v1/token",
        url:"http://139.155.144.42:8000/v1/token",
        // 把JS的对象或数组序列化一个json 字符串
        data:JSON.stringify(post_data),
        // result 为请求的返回结果对象
        success:function (result) {
            if (200 == result.code){
                window.localStorage.setItem('dnblog_token', result.data.token)
                window.localStorage.setItem('dnblog_nickname', result.nickname)
                window.localStorage.setItem('dnblog_email', result.email)
                alert('登录成功')
                //取本会话的上一跳
                refer_url = document.referrer
                //如果是项目内部的请求，回跳到上一步
                if (refer_url.search('127.0.0.1') != -1){
                    window.location = refer_url;
                    console.log('refer_url=',refer_url)
                }else{
                    window.location =  '/';
                    console.log('/')
                }
            }else{
                alert(result.error)
            }
        }
    });
}
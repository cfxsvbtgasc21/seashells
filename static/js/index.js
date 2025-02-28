/*from image_display.html*/

// 定义需要删除的文件路径列表
    const filesToDelete = { files_to_delete,tojson };

// 页面加载时，检查是否是刷新操作
window.addEventListener("load", function () {
    if (sessionStorage.getItem("isRefreshing")) {
        window.location.href = document.referrer || "/";
        sessionStorage.removeItem("isRefreshing");
    } else {
        window.addEventListener("beforeunload", function (e) {
            fetch("/delete_files", {
                method: "POST", headers: {
                    "Content-Type": "application/json",
                }, body: JSON.stringify({file_paths: filesToDelete}),
            })
                .then(response => response.json())
                .then(data => console.log("Files deleted:", data))
                .catch(error => console.error("Error deleting files:", error));
        });
    }
});

window.addEventListener("beforeunload", function () {
    sessionStorage.setItem("isRefreshing", "true");
});


/*from register.html*/
	// js正则验证相关字符的意义
	// 1.  /^$/ 这个是个通用的格式。
	// ^ 匹配输入字符串的开始位置；$匹配输入字符串的结束位置
    // 2. 里面输入需要实现的功能。
    // * 匹配前面的子表达式零次或多次；
    // + 匹配前面的子表达式一次或多次；
    // ？匹配前面的子表达式零次或一次；
    // \d  匹配一个数字字符，等价于[0-9]
/*        window.onload = function(){
        document.getElementById("form").onsubmit = function(){
                return checkUsername() && checkPassword() && checkPassword2() && mailbox() && checkMobilePhone() && imgCode();
        };
            document.getElementById("username").onblur = checkUsername;
            document.getElementById("password").onblur = checkPassword;
            document.getElementById("password2").onblur = checkPassword2;
            document.getElementById("email").onblur = mailbox; 
            document.getElementById("telphone").onblur = checkMobilePhone; 
             document.getElementById("checkcode").onblur = imgCode; 
        }            
        function checkUsername(){
            //固定六位到十位字符用户名包含大小写字母与数字的组合
            var username = document.getElementById("username").value;
            var reg_username =/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,10}$/;
            var flag = reg_username.test(username);
            var s_username = document.getElementById("s_username");
            if(flag){
                s_username.innerHTML = "<img width='35' height='25' src='../images/right.png'/>";
                return true;
            }else{
                s_username.innerHTML = "用户名格式有误";
                return false;
            }
            
        }
		
        function checkPassword(){
            //固定六位到十位字符密码包含大小写字母与数字的组合，当然你也可以改变正则方式，详情可见https://www.jb51.net/article/115170.htm
            var password = document.getElementById("password").value;
            var reg_password = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,10}$/;
            var flag = reg_password.test(password);
            var s_password = document.getElementById("s_password");
            if(flag){
                s_password.innerHTML = "<img width='35' height='25' src='../images/right.png'/>";
                return true;
            }else{
                s_password.innerHTML = "密码格式有误";
                return false;
            }
        }

        function checkPassword2(){
            //与上步的password正则验证一样，加了个密码一致的匹配
            var password2 = document.getElementById("password2").value;
            var reg_password2 = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,10}$/;
            var flag = reg_password2.test(password2);
            var s_password2 = document.getElementById("s_password2");
            if(flag && password2 == document.getElementById("password").value){
                s_password2.innerHTML = "<img width='35' height='25' src='../images/right.png'/>";
                 return true;
            }else{
                s_password2.innerHTML = "密码格式不一致";
                return false;
            }
        }

        function mailbox(){
        //定义正则表达式的变量:邮箱正则邮箱地址 必须由 大小写字母 或 数字 或下划线开头，其后可以跟上任意的 \w字符 和 中划线 加号 英文句号 @ 跟上任意的 \w字符 和 中划线(-) 加号 英文句号(.)
        var email =document.getElementById("email").value; 
        var emailReg=/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
         var flag = emailReg.test(email);
         var test_email = document.getElementById("test_email");
        if(flag)
        {
             test_email.innerHTML = "<img width='35' height='25' src='../images/right.png'/>";
              return true;
        }else{
             test_email.innerHTML = "邮箱格式有误";
              return false;
        }
     }   
        function checkMobilePhone() {
             //定义正则表达式的变量:1.手机号正则，/^[1][3,4,5,6,7,8,9][0-9]{9}$/ //2.电话号码正则：/^(([0\+]\d{2,3}-)?(0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$/
             //手机号正则表达式的意思是：以1为开头,第二位可为3,4,5,6,7,8,9,中的任意一位,最后以0-9的9个整数结尾。
             //电话号码正则,你懂的就是区号加后面几位用户号码
        var telphone = document.getElementById("telphone").value; 
        var phoneReg= /^[1][3,4,5,6,7,8,9][0-9]{9}$/;
        var flag = phoneReg.test(telphone);
        var mobile_input = document.getElementById("mobile_input");
         if(flag)
        {
             mobile_input.innerHTML = "<img width='35' height='25' src='../images/right.png'/>";
             return true;
        }else{
             mobile_input.innerHTML = "电话号码格式有误";
             return false;
        }
        }   

         function imgCode(){
            //为了偷懒，写了个固定的验证码，验证码可以是动态改变，也可以静态更换，静态的利用js，用一个数组将验证码图片存起来//当用户点击更换验证码图片时，触发onclick事件更新验证码，用户可输入不同的验证码进行登录，但这样账号的安全性极其//的低(毕竟是前端验证🤣🤣🤣)
            var get_img=document.getElementById("checkcode").value;
           if(get_img== "7427"){
             code_input.innerHTML = "<img width='35' height='25' src='../images/close.png'/>";
             return true;
           }
           else {
            code_input.innerHTML = "验证码输入有误，请重新输入";
            return false;
           }
         }

        function checkform(){
            //表单总确认
       if(checkUsername() && checkPassword () && checkPassword2() && mailbox() && checkMobilePhone() && imgCode()==true){
        window.alert("恭喜您！注册成功");
        return true;
       }else{
        window.alert("请您核对一下您的注册信息是否有误");
        return false;
       }

    }

       //获取ID内容
      var eye1 = document.getElementById('eye1');
      var password = document.getElementById('password');
      var flag1 = 0;
          //触发点击事件 处理程序
      eye1.onclick = function(){
          //点击一次后 flag一定要变化
          if (flag1 == 0){
              password.type = 'text';
              eye1.src="{{url_for('static',filename='images/open.png')}}";
              flag1 = 1;
          }else{
              password.type = 'password';
              eye1.src="{{url_for('static',filename='images/close.png')}}";
              flag1 = 0;
          }
      }
	  var eye2 = document.getElementById('eye2');
      var password2 = document.getElementById('password2');
      var flag2 = 0;
          //注册事件 处理程序
      eye2.onclick = function(){
          //点击一次后 flag一定要变化
          if (flag2 == 0){
              password2.type = 'text';
              eye2.src="{{url_for('static',filename='images/open.png')}}";
              flag2 = 1;
          }else{
              password2.type = 'password';
              eye2.src="{{url_for('static',filename='images/close.png')}}";
              flag2 = 0;
          }
      }
#2020-2-27
>>1、登陆界面input框不能输入  
uikit.min.css默认使用uk-from-icon的属性pointer-events: none；因此表框无法点击。 
在head中添加  
	&lt;style type=text/css>
	    input {
	        pointer-events: auto;
	    }
	</style&gt;

>>2、多次注册一直显示email值错误  
在_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')中通过正则表达式匹配邮箱时‘+’前后不能加空格。

>>3、/api/authenticate是一个POST请求，错误绑定成GET，导致浏览器出现405错误。


#2020-2-28
>>1、后端获取不到数据，保存日志只刷新页面不跳转到/api/blogs
event.preventDefault() 函数写错。  
在用jQuery给button绑定事件的时候， 在form表单中 button会有一个会自动刷新页面的默认行为
使用event.preventDefault() 函数取消自动刷新页面的默认行为  
我的理解 ：每点一次“保存”都会刷新页面 ， 浏览器会再次发出一个GET请求，原url，
后端都会一直进入处理该url的函数中，而导致不能接受到输入的数据。而且每次刷新都会清除输入的数据。

>>2、v-repeat写错造成浏览器不能显示添加的日志信息。
把v-repeat="blog:blogs"看成循环代码，可以在一个	tr标签内部引用循环变量blog

>>3、发现在location.assign('/manage/blogs' );中path末尾不能加/ 比如像这样location.assign('/manage/blogs/' );看似没错结合后端看，定义的是@get('/manage/blogs')，是没有这个url对应的处理函数

#2020-2-29 
>>1、extend()函数的作用  
在已存在的列表中添加新的列表内容。

>>2、不能删除日志  
没有登录用户，没获取到管理员身份。

>>3、再次出现405错误，Method Not Allowed  
有浏览器url的处理函数，后来发现是没有对html文件中 getJSON 提交的url进行处理。  

#2020-3-1  
>>导入Fabric API时报错ImportError: No module named api  
>>高版本把这个模块移除了，安装个低版本.pip install fabric==1.14.0  

#2020-3-2  
>>Supervisor启动app.py是报错没有python库？
>>用su命令进入root用户再pip3安装  

#2020-3-3
>>1、 nginx启动不成功 ？  
>>使用 nginx-t 查看出现nginx: [emerg] directive "location" has no opening "{" in /etc/nginx/sites-enabled/default:14
>>意思是在14行的'{'前面没加'空格'  

>>2、访问服务器时只显示hello页面  
>>解决方法：将default配置文件中的端口改了  

#2020-3-4  
>>1、javascript中 $('#vm')的意思是获取页面中id为vm的对象  

>>2、javascript中var是用于声明变量  

>>3、javascript中Vue 是简单易用的MVVM(Model View ViewMode)框架;  

>>>>el：element，需要获取的对应元素，html中的容器，（id名）
>>>>data：数据存储，里面的值自己设置;data里的参数会传入el: id名对应的容器中  

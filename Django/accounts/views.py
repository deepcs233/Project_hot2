# coding=utf-8
# django package
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import base64
import re
import datetime
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
import json
import platform
from .models import UserPostInfo,UserWatchTag
from forms import RegisterForm





# Create your views here.
ALLOW_CHAR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
SECRET_KEY = 'v65p7r0#gd3&56we-eus82!ch_0l+0gb%r6rzm(yy$amp#mps$'

def register(request):
    '''注册视图'''
    template_var = {}
    form = RegisterForm()
    if request.method == "POST":
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST=json.loads(request.body)#['username']

        form = RegisterForm(request.POST.copy())

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()

            newone = UserPostInfo(user=user, email=email, acceptPost= 0)
            newone.save()

            try:
                send_mail(u'点击邮件内链接完成注册！',u'请点击下方的链接，如不能打开请将地址复制到浏览器后再次打开：\n        '+getCipherUrl(user.username),
                          'dailynews@hottestdaily.com',[email])
            except:
                return JsonResponse(({'errorCode':1,'errorMsg':[u'邮件发送失败，请重试或者更换邮箱']}))

            return JsonResponse(({'errorCode': 0,'errorMsg':""}))
            #if _login(request, username, password, template_var):
            #    return HttpResponseRedirect("/monitor/index")
        errorMsg=[]
        for each in form.errors:
            errorMsg+=form.errors[each]

        return JsonResponse({'errorCode':1,'errorMsg':errorMsg})
    template_var["form"] = form

    return JsonResponse(({'errorCode': 0, 'errorMsg': ""}))

#!forms.py form.errors
#@ensure_csrf_cookie
def login(request):
    '''登陆视图'''
    from django.contrib.auth.hashers import make_password
    print make_password('123456')
    template_var = {}
    if request.method == 'POST':
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST=json.loads(request.body)#['username']
        username = request.POST.get("username")
        password = request.POST.get("password")
        if _login(request, username, password, template_var):
            return JsonResponse(({'errorCode': 0, 'errorMsg': ""}))
        else:
            return JsonResponse({'errorCode': 1, 'errorMsg':  template_var['error']})


    return JsonResponse(({'errorCode': 0, 'errorMsg': ""}))


def _login(request, username, password, dict_var):
    '''登陆核心方法'''
    ret = False

    if len(User.objects.filter(username=username))==0:
        dict_var['error']= u'用户' + username + u'不存在'
        return False
    else:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                ret = True
            else:
                dict_var["error"] = u'用户' + username + u'没有激活'
        else:
            dict_var["error"] = u'用户名或密码错误'
        return ret


def logout(request):
    try:
        auth_logout(request)
        return JsonResponse(({'errorCode': 0, 'errorMsg': ""}))
    except:
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})

def captcha(request):#获取验证码，并发送至邮箱
    if request.method=='POST':
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username']



        if 'username' in request.POST:
            username=request.POST['username']
            user=User.objects.filter(username=username)[0]
            receiver=user.email

        elif  'email' in request.POST:
            email=request.POST['email']
            user=User.objects.filter(email=email)[0]
            username=user.username
            receiver=email
        else:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})

        captcha = buildCaptcha(username)

        try:
            send_mail(u'来自WebMonitor的验证码', u'   您的验证码为' + captcha,'dailynews@hottestdaily.com',[receiver])
            return JsonResponse({'errorCode':0,'errorMsg':""})
        except:
            return JsonResponse(({'errorCode': 1, 'errorMsg': u'邮件发送失败，请重试或者更换邮箱'}))
        #    return JsonResponse({'status': 'ERROR','detail':u'邮件发送失败'})




def active_user(request,ciphertext):

    t=base64.b64decode(ciphertext)
    try:
        username=re.findall(r'webmonitor(.+)ZZ',t)[0]
        user=User.objects.filter(username=username)[0]
    except:
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
    user.is_active=True
    user.save()
    return HttpResponseRedirect("/index.html")

def fgPasswd(request):#接受验证码，如果符合则成功修改密码
    if request.method == 'POST':
        try:
            # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
            request.POST = json.loads(request.body)  # ['username']

            if ('email' not in request.POST) or ('captcha' not in request.POST) or ('password' not in request.POST):
                return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
            user=User.objects.filter(email=request.POST['email'])[0]
            username=user.username
            captcha=buildCaptcha(username)
            if captcha==request.POST['captcha']:


                passwd=request.POST['password']
                for each in passwd:
                    if each not in ALLOW_CHAR:
                        return JsonResponse({'errorCode': 1, 'errorMsg': u'出现非法字符'})
                if len(passwd)<6:
                    return JsonResponse({'errorCode': 1, 'errorMsg': u'密码长度小于6个字符'})
                if len(passwd)>20:
                    return JsonResponse({'errorCode': 1, 'errorMsg': u'密码长度大于20个字符'})

                user.password=make_password(passwd)
                user.save()

                return JsonResponse({'errorCode': 0,'errorMsg':""})
                #auth_login(request, user)
                #return HttpResponseRedirect("/monitor/index")

            else:
                return JsonResponse({'errorCode': 1, 'errorMsg':u'验证码输入错误'})
        except Exception,e:
            print e
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
    else:
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})


def getLoginStatus(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            return JsonResponse({'errorCode':0,'username':request.user.username})
        else:
            return JsonResponse({'errorCode':0,'username':''})
    else:
        return JsonResponse({'errorCode':1,'errorMsg':u'未知错误'})

@login_required
def getUserInfo(request):
    if request.method == 'POST':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else :
        data = { }
        t = UserPostInfo.objects.filter(user = request.user)[0]
        data['errorCode'] = 0
        data['email'] = t.email
        data['acceptPost'] = t.acceptPost
        data['username'] = User.objects.filter(user = request.user)[0].username
        return JsonResponse(data)

@login_required
def getUsername(request):
    if request.method == 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username'
        user = User.objects.filter(user = request.user)[0]
        if 'username' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
        username = request.POST.get('username')

        if len(username) < 3 or len(username) > 20:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'用户名长度需要在3-20字符内'})

        for char in username:
            if char not in ALLOW_CHAR:
                return JsonResponse({'errorCode': 1, 'errorMsg': u'用户名中出现了非法字符'})

        if  username == (User.objects.filter(user = request.user)[0]).username:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'与原用户名相同'})

        if len(User.objects.filter(username = username)) > 0:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'该用户名已存在'})

        user.username = username
        user.save()
        return JsonResponse({'errorCode': 0,})

    
@login_required
def editUsername(request):
    if request.method == 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username'

        if 'username' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
        username = request.POST.get('username')
        
        if (User.objects.filter(user = request.user)[0]).username == username:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'与原用户名相同'})

        if len(User.objects.filter(username = username)) > 0:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'该用户名已被使用'})

        user = User.objects.filter(user = request.user)[0]

        user.username = username

        user.save()

        return JsonResponse({'errorCode': 0,})
    
@login_required
def editUserMail(request):
    if request.method == 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username'


        if 'email' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
        email = request.POST.get('email')


        if  email == (UserPostInfo.objects.filter(user = request.user)[0]).email:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'与原邮箱相同'})

        user = UserPostInfo.objects.filter(user = request.user)[0]
        user.email = email
        user.save()
        return JsonResponse({'errorCode': 0,})

@login_required
def editUserAcceptPost(request):
    if request.method == 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username'

        if 'acceptPost' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})

        acceptPost = request.POST.get('acceptPost')
        if acceptPost == 1 or acceptPost == 0:
            user = UserPostInfo.objects.filter(user = request.user)[0]
            user.acceptPost = acceptPost
            user.save()
        else:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})

@login_required
def addWatchTag(request):
    if request.method == 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username'

        if 'data' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
        tag = request.POST['data']

        if len(tag) > 6 or len(tag) < 2 :
            return  JsonResponse({'errorCode': 1, 'errorMsg': u'词语长度需在2-4字之间'})

        if len(UserWatchTag.objects.filter(user = request.user , word = tag)) > 0:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'用户已添加过此词语'})

        new = UserWatchTag(user = request.user, word = tag)
        new.save()
        return JsonResponse({'errorCode': 0,})

@login_required
def getWatchList(request):
    if request.method != 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        t = {}
        data = []
        for each in UserWatchTag.objects.filter(user = request.user):
            data.append(each.word)
        t['errorCode'] = 0
        t['data'] = data

        return JsonResponse(t)

@login_required
def delWatchTag(request):
    if request.method == 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username'

        if 'data' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
        tag = request.POST['data']

        tt = UserWatchTag.objects.filter(user = request.user,word = tag)
        if len(tt) > 0:
            tt.delete()
            return JsonResponse({'errorCode': 0,})
        else:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'该用户没有关注此词语'})




def getCipherUrl(username):
    
    cipher=base64.b64encode('webmonitor'+username+'ZZ'+SECRET_KEY)
    if platform.system() == 'Linux':
        return  'http://www.hottestdaily.com/accounts/active='+cipher
    if platform.system() == 'Windows':
        return  'http://127.0.0.1:8000/accounts/active='+cipher

def buildCaptcha(username):

    n = 0

    for each in username:
        n += ord(each)

    while (n <= 10000):
        n = n * n

    n=n*datetime.datetime.now().day
    n = str(n % 10000)

    for i in range(4 - len(n)):
        n = '0' + n

    return n


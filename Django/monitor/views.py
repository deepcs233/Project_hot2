#encoding=utf-8
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import  JsonResponse
from .models import UserToUrls
import json

@login_required
def addWatchUrl(request):
    if request.method == 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username'

        if 'data' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
        url = request.POST['data']

        if len(url) > 100:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'添加的此url长度大于100字符'})

        if len(UserToUrls.objects.filter(user = request.user ,url = url)) > 0:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'该用户已添加此url'})

        new = UserToUrls(user = request.user,url = url)
        new.save()
        return JsonResponse({'errorCode': 0,})


@login_required
def delWatchUrl(request):
    if request.method == 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username'

        if 'data' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
        url = request.POST['data']

        if len(url) > 100:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'添加的此url长度大于100字符'})

        if len(UserToUrls.objects.filter(user=request.user, url=url)) == 0:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'该用户没有添加此url'})

        UserToUrls.objects.filter(user=request.user, url=url).delete()
        return JsonResponse({'errorCode': 0,})


@login_required
def getWatchUrl(request):
    if request.method != 'GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误'})
    else:
        t = {}
        t['errorCode'] = 0
        data = []

        for each in UserToUrls.objects.filter(user = request.user):
            data.append(each.url)

        return JsonResponse(t)

@login_required
def getWatchThing(request):
    pass

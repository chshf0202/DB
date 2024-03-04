from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *
from app.views.Picture import *
from datetime import datetime
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import jwt
from foodSite.settings import SECRET_KEY

BLANK_USER_PICTURE_ID = 'p0000000'


class AddUser(APIView):
    UidBase = 1

    def post(self, request):
        ret = 0
        message = '注册成功'
        Uid = 'u' + str(AddUser.UidBase).zfill(7)
        AddUser.UidBase += 1
        Uname = request.data['Uname']
        phone = request.data['phone']
        pwd = request.data['pwd']
        if User.objects.filter(Uname=Uname).exists():
            ret = 1
            message = '用户名已注册'
            return Response({'value': ret, 'message': message})
        if User.objects.filter(phone=phone).exists():
            ret = 2
            message = '手机号已注册'
            return Response({'value': ret, 'message': message})
        try:
            Pid = Picture.objects.get(Pid=BLANK_USER_PICTURE_ID)
            user = User.objects.create(Uid=Uid, Uname=Uname, phone=phone, pwd=pwd, Pid=Pid)
            user.save()
        except Picture.DoesNotExist:
            ret = 4
            message = '图片未找到'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 3
            message = '注册失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})


class LoginUserName(APIView):
    @csrf_exempt
    def post(self, request):
        Uname = request.data['Uname']
        pwd = request.data['pwd']
        try:
            user = User.objects.get(Uname=Uname)
            if user.pwd != pwd:
                ret = 2
                message = '密码错误'
                return Response({'value': ret, 'message': message})
            token_payload = {
                'user_id': user.Uid,
                'username': user.Uname,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
            if user.Uid == 'u0000000':
                picture = None
                response_data = {
                    'value': 0,
                    'message': '管理员登录成功',
                    'data': {
                        'token': token,
                        'expireAt': (datetime.utcnow() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                        'user': {
                            'id': user.Uid,
                            'password': user.pwd,
                            'name': user.Uname,
                            'picture': picture,
                            'phone': user.phone,
                        },
                        'permissions': [],  # 根据实际情况设置权限列表
                        'roles': ['admin']  # 根据实际情况设置角色列表
                    },
                    'Pid': user.Pid.Pid,
                }
                return Response(response_data)
            else:
                if user.Pid.Pid == 'p0000000':
                    picture = None
                else:
                    picture = Picture.objects.get(Pid=user.Pid.Pid).path
        except User.DoesNotExist as e:
            print(e)
            ret = 1
            message = '用户名未注册'
            return Response({'value': ret, 'message': message})
        except Picture.DoesNotExist as e:
            print(e)
            ret = 3
            message = '用户图片错误'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 4
            message = '登录失败'
            return Response({'value': ret, 'message': message})
        response_data = {
            'value': 0,
            'message': '用户登录成功',
            'data': {
                'token': token,
                'expireAt': (datetime.utcnow() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                'user': {
                    'id': user.Uid,
                    'password': user.pwd,
                    'name': user.Uname,
                    'picture': picture,
                    'phone': user.phone,
                },
                'permissions': [],  # 根据实际情况设置权限列表
                'roles': []  # 根据实际情况设置角色列表
            },
            'Pid': user.Pid.Pid,
        }
        return Response(response_data)


class LoginUserPhone(APIView):
    @csrf_exempt
    def post(self, request):
        phone = request.data['phone']
        pwd = request.data['pwd']
        try:
            user = User.objects.get(phone=phone)
            if user.pwd != pwd:
                ret = 2
                message = '密码错误'
                return Response({'value': ret, 'message': message})
            token_payload = {
                'user_id': user.Uid,
                'username': user.Uname,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
            if user.Uid == 'u0000000':
                picture = None
                response_data = {
                    'value': 0,
                    'message': '管理员登录成功',
                    'data': {
                        'token': token,
                        'expireAt': (datetime.utcnow() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                        'user': {
                            'id': user.Uid,
                            'password': user.pwd,
                            'name': user.Uname,
                            'picture': picture,
                            'phone': user.phone,
                        },
                        'permissions': [],  # 根据实际情况设置权限列表
                        'roles': ['admin']  # 根据实际情况设置角色列表
                    },
                    'Pid': user.Pid.Pid,
                }
                return Response(response_data)
            else:
                if user.Pid.Pid == 'p0000000':
                    picture = None
                else:
                    picture = Picture.objects.get(Pid=user.Pid.Pid).path
        except User.DoesNotExist as e:
            print(e)
            ret = 1
            message = '手机号未注册'
            return Response({'value': ret, 'message': message})
        except Picture.DoesNotExist as e:
            print(e)
            ret = 3
            message = '用户图片错误'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 4
            message = '登录失败'
            return Response({'value': ret, 'message': message})
        response_data = {
            'value': 0,
            'message': '用户登录成功',
            'data': {
                'token': token,
                'expireAt': (datetime.utcnow() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                'user': {
                    'id': user.Uid,
                    'password': user.pwd,
                    'name': user.Uname,
                    'picture': picture,
                    'phone': user.phone,
                },
                'permissions': [],  # 根据实际情况设置权限列表
                'roles': []  # 根据实际情况设置角色列表
            },
            'Pid': user.Pid.Pid,
        }
        return Response(response_data)


class UploadUserPicture(APIView):
    def post(self, request):
        ret = 0
        message = '图片上传成功'
        Uid = request.data['Uid']
        picture = request.data['picture']
        Pid = getId()
        try:
            picture = Picture.objects.create(Pid=Pid, path=picture)
            picture.save()
            user = User.objects.get(Uid=Uid)
            user.Pid = picture
            user.save()
        except User.DoesNotExist:
            ret = 1
            message = '用户未找到'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 2
            message = '图片上传失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})


class ChangeUserPwd(APIView):
    def post(self, request):
        ret = 0
        message = '修改密码成功'
        Uid = request.data['Uid']
        pwd = request.data['pwd']
        try:
            user = User.objects.get(Uid=Uid)
            user.pwd = pwd
            user.save()
        except User.DoesNotExist:
            ret = 1
            message = '用户未找到'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 2
            message = '修改密码失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})


class ChangeUserUname(APIView):
    def post(self, request):
        ret = 0
        message = '修改用户名成功'
        Uid = request.data['Uid']
        Uname = request.data['Uname']
        try:
            if User.objects.filter(Uname=Uname).exists():
                ret = 1
                message = '用户名已注册'
                return Response({'value': ret, 'message': message})
            user = User.objects.get(Uid=Uid)
            user.Uname = Uname
            user.save()
        except User.DoesNotExist:
            ret = 2
            message = '用户未找到'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 3
            message = '修改用户名失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})


class ChangeUserPhone(APIView):
    def post(self, request):
        ret = 0
        message = '修改手机号成功'
        Uid = request.data['Uid']
        phone = request.data['phone']
        try:
            if User.objects.filter(phone=phone).exists():
                ret = 1
                message = '手机号已注册'
                return Response({'value': ret, 'message': message})
            user = User.objects.get(Uid=Uid)
            user.phone = phone
            user.save()
        except User.DoesNotExist:
            ret = 2
            message = '用户未找到'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 3
            message = '修改手机号失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})


class StarDish(APIView):
    def post(self, request):
        ret = 0
        message = '收藏成功'
        Uid = request.data['Uid']
        Did = request.data['Did']
        try:
            user = User.objects.get(Uid=Uid)
            dish = Dish.objects.get(Did=Did)
            if UserStarDish.objects.filter(Uid=user, Did=dish).exists():
                ret = 1
                message = '菜品已收藏'
                return Response({'value': ret, 'message': message})
            else:
                dish.star += 1
                dish.save()
                star = UserStarDish.objects.create(Uid=user, Did=dish)
                star.save()
        except User.DoesNotExist:
            ret = 2
            message = '用户未找到'
            return Response({'value': ret, 'message': message})
        except Dish.DoesNotExist:
            ret = 3
            message = '菜品未找到'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 4
            message = '收藏失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})


class UnstarDish(APIView):
    def post(self, request):
        ret = 0
        message = '取消收藏成功'
        Uid = request.data['Uid']
        Did = request.data['Did']
        try:
            user = User.objects.get(Uid=Uid)
            dish = Dish.objects.get(Did=Did)
            if not UserStarDish.objects.filter(Uid=user, Did=dish).exists():
                ret = 1
                message = '菜品未收藏'
                return Response({'value': ret, 'message': message})

            else:
                dish.star -= 1
                dish.save()
                star = UserStarDish.objects.get(Uid=user, Did=dish)
                star.delete()
        except User.DoesNotExist:
            ret = 2
            message = '用户未找到'
            return Response({'value': ret, 'message': message})
        except Dish.DoesNotExist:
            ret = 3
            message = '菜品未找到'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 4
            message = '取消收藏失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})


class GetStar(APIView):
    def post(self, request):
        Uid = request.data['Uid']
        Did = request.data['Did']
        try:
            user = User.objects.get(Uid=Uid)
            dish = Dish.objects.get(Did=Did)
            if UserStarDish.objects.filter(Uid=user, Did=dish).exists():
                isStared = True
            else:
                isStared = False
        except User.DoesNotExist:
            ret = 1
            message = '用户未找到'
            return Response({'value': ret, 'message': message})
        except Dish.DoesNotExist:
            ret = 2
            message = '菜品未找到'
            return Response({'value': ret, 'message': message})
        return Response({'isStared': isStared})


class GetUserInfo(APIView):
    def get(self, request):
        Uid = request.GET['Uid']
        try:
            user = User.objects.get(Uid=Uid)
            picture = Picture.objects.get(Pid=user.Pid.Pid).path
            return Response({'Uname': user.Uname, 'phone': user.phone,
                             'pwd': user.pwd, 'picture': picture})
        except User.DoesNotExist:
            ret = 1
            message = '找不到用户'
            return Response({'ret': ret, 'message': message})
        except Picture.DoesNotExist:
            ret = 2
            message = '找不到图片'
            return Response({'ret': ret, 'message': message})

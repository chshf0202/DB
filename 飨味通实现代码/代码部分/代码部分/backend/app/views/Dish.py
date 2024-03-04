from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *
from app.views.Picture import *


class GetDishDisplay(APIView):
    def get(self, request):
        dishList = Dish.objects.all().order_by('Did')
        ans = []
        for dish in dishList:
            try:
                picture = Picture.objects.get(Pid=dish.Pid.Pid).path
                ans.append({'Did': dish.Did, 'Dname': dish.Dname,
                            'price': dish.price, 'description': dish.description,
                            'score': dish.score, 'star': dish.star,
                            'remain': dish.remain, 'Gid': dish.Gid.Gid,
                            'picture': picture, 'quantity': 0})
            except Picture.DoesNotExist:
                ret = 1
                message = '图片未找到'
                return Response({'value': ret, 'message': message})
        return Response({'dishList': ans})


class GetDishWithTag(APIView):
    def get(self, request):
        dishList = Dish.objects.all().order_by('Did')
        ans = []
        for dish in dishList:
            try:
                picture = Picture.objects.get(Pid=dish.Pid.Pid).path
                tagList = []
                DishTagList = DishTag.objects.filter(Did=dish)
                for dishTag in DishTagList:
                    tag = Tag.objects.get(Tid=dishTag.Tid.Tid)
                    tagList.append({'Tid': dishTag.Tid.Tid, 'Tname': tag.Tname})
                ans.append({'Did': dish.Did, 'Dname': dish.Dname,
                            'price': dish.price, 'description': dish.description,
                            'score': dish.score, 'star': dish.star,
                            'remain': dish.remain, 'Gid': dish.Gid.Gid,
                            'picture': picture, 'quantity': 0,
                            'tagList': tagList})
            except Picture.DoesNotExist:
                ret = 1
                message = '图片未找到'
                return Response({'value': ret, 'message': message})
        return Response({'dishList': ans})


class AddDish(APIView):
    DidBase = 0

    def post(self, request):
        ret = 0
        message = '添加菜品成功'
        Did = 'd' + str(AddDish.DidBase).zfill(7)
        AddDish.DidBase += 1
        Dname = request.data['Dname']
        price = request.data['price']
        description = request.data['description']
        score = 0
        star = 0
        remain = request.data['remain']
        Gid = request.data['Gid']
        if Dish.objects.filter(Dname=Dname).exists():
            ret = 1
            message = '菜品已注册'
            return Response({'value': ret, 'message': message})
        try:
            group = Group.objects.get(Gid=Gid)
            picture = Picture.objects.create(Pid=getId(), path=request.data['picture'])
            picture.save()
            dish = Dish.objects.create(Did=Did, Dname=Dname, price=price,
                                       description=description, score=score,
                                       star=star, remain=remain, Pid=picture,
                                       Gid=group)
            dish.save()
        except Group.DoesNotExist:
            ret = 2
            message = '菜品组未找到'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 3
            message = '添加菜品失败'
        return Response({'value': ret, 'message': message})


class AddDishRemain(APIView):
    def post(self, request):
        ret = 0
        message = '添加菜品余量成功'
        Did = request.data['Did']
        number = request.data['number']
        try:
            dish = Dish.objects.get(Did=Did)
            dish.remain = int(dish.remain) + int(number)
            dish.save()
        except Dish.DoesNotExist as e:
            print(e)
            ret = 1
            message = '找不到菜品'
        except Exception as e:
            print(e)
            ret = 2
            message = '添加菜品余量失败'
        return Response({'value': ret, 'message': message})


class AddDishTag(APIView):
    def post(self, request):
        ret = 0
        message = '添加菜品标签成功'
        Did = request.data['Did']
        TidList = request.data['TidList']
        for Tid in TidList:
            try:
                dish = Dish.objects.get(Did=Did)
                tag = Tag.objects.get(Tid=Tid)
                dishTag = DishTag.objects.create(Did=dish, Tid=tag)
                dishTag.save()
            except Dish.DoesNotExist:
                ret = 1
                message = '菜品未找到'
                return Response({'value': ret, 'message': message})
            except Dish.DoesNotExist:
                ret = 2
                message = '标签未找到'
                return Response({'value': ret, 'message': message})
            except Exception as e:
                print(e)
                ret = 3
                message = '添加菜品标签失败'
        return Response({'value': ret, 'message': message})


class GetUserOrderedDish(APIView):
    def get(self, request):
        Uid = request.GET['Uid']
        ans = []
        user = User.objects.get(Uid=Uid)
        orderList = Order.objects.filter(Uid=user)
        Dids = []
        for order in orderList:
            orderedDishes = DishOrder.objects.filter(Oid=order.Oid)
            for orderedDish in orderedDishes:
                if orderedDish.Did.Did not in Dids:
                    Dids.append(orderedDish.Did.Did)
                    try:
                        dish = Dish.objects.get(Did=orderedDish.Did.Did)
                        picture = Picture.objects.get(Pid=dish.Pid.Pid).path
                        ans.append({'Did': dish.Did, 'Dname': dish.Dname,
                                'price': dish.price, 'description': dish.description,
                                'score': dish.score, 'star': dish.star,
                                'remain': dish.remain, 'Gid': dish.Gid.Gid,
                                'picture': picture})
                    except Dish.DoesNotExist:
                        ret = 1
                        message = '菜品未找到'
                        return Response({'value': ret, 'message': message})
        return Response({'dishList': ans})

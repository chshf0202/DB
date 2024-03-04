from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *
from datetime import date


class GetUserOrder(APIView):
    def get(self, request):
        Uid = request.GET['Uid']
        ans = []
        try:
            user = User.objects.get(Uid=Uid)
            orderList = Order.objects.filter(Uid=user)
            for order in orderList:
                dishNumber = {}
                dishOrders = DishOrder.objects.filter(Oid=order.Oid)
                for dishOrder in dishOrders:
                    if dishOrder.Did.Did in dishNumber:
                        dishNumber[dishOrder.Did.Did] = int(dishNumber.get(dishOrder.Did.Did)) + int(dishOrder.number)
                    else:
                        dishNumber[dishOrder.Did.Did] = int(dishOrder.number)
                dishList = []
                for Did, number in dishNumber.items():
                    dish = Dish.objects.get(Did=Did)
                    picture = Picture.objects.get(Pid=dish.Pid.Pid).path
                    dishList.append({'Did': Did, 'number': number, 'picture': picture})
                ans.append({'Oid': order.Oid, 'total': order.total,
                            'time': order.time.strftime('%Y-%m-%d'), 'dishList': dishList})
            return Response({'orderList': ans})
        except User.DoesNotExist:
            ret = 1
            message = '用户未找到'
            return Response({'value': ret, 'message': message})
        except Dish.DoesNotExist:
            ret = 2
            message = '菜品未找到'
            return Response({'value': ret, 'message': message})
        except Picture.DoesNotExist:
            ret = 3
            message = '图片未找到'
            return Response({'value': ret, 'message': message})


class AddOrder(APIView):
    OidBase = 0

    def post(self, request):
        ret = 0
        message = '下单成功'
        Oid = 'o' + str(AddOrder.OidBase).zfill(7)
        AddOrder.OidBase += 1
        Uid = request.data['Uid']
        total = request.data['total']
        dishList = request.data['dishList']
        try:
            user = User.objects.get(Uid=Uid)
            order = Order.objects.create(Oid=Oid, Uid=user, total=total, time=date.today())
            order.save()
            for dish in dishList:
                Did = dish['Did']
                number = dish['number']
                dish = Dish.objects.get(Did=Did)
                dish.remain = int(dish.remain) - int(number)
                dish.save()
                dishOrder = DishOrder.objects.create(Oid=order, Did=dish, number=number)
                dishOrder.save()
        except User.DoesNotExist:
            ret = 1
            message = '用户未找到'
            return Response({'value': ret, 'message': message})
        except Dish.DoesNotExist:
            ret = 2
            message = '菜品未找到'
            return Response({'value': ret, 'message': message})
        except Exception as e:
            print(e)
            ret = 3
            message = '点菜失败'
        return Response({'value': ret, 'message': message})

from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *


class GetDishTag(APIView):
    def post(self, request):
        Did = request.data['Did']
        ans = []
        try:
            dish = Dish.objects.get(Did=Did)
            DishTagList = DishTag.objects.filter(Did=dish)
            for dishTag in DishTagList:
                tag = Tag.objects.get(Tid=dishTag.Tid.Tid)
                ans.append({'Tid': dishTag.Tid.Tid, 'Tname': tag.Tname})
            return Response({'tagList': ans})
        except Dish.DoesNotExist:
            ret = 1
            message = '菜品未找到'
            return Response({'value': ret, 'message': message})
        except Tag.DoesNotExist:
            ret = 2
            message = '标签未找到'
            return Response({'value': ret, 'message': message})


class AddTag(APIView):
    TidBase = 0

    def post(self, request):
        ret = 0
        message = '添加标签成功'
        Tid = 't' + str(AddTag.TidBase).zfill(7)
        AddTag.TidBase += 1
        Tname = request.data['Tname']
        try:
            tag = Tag.objects.create(Tid=Tid, Tname=Tname)
            tag.save()
        except Exception as e:
            print(e)
            ret = 1
            message = '添加标签失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})


class GetAllTag(APIView):
    def get(self, request):
        ans = []
        tagList = Tag.objects.all().order_by('Tid')
        for tag in tagList:
            ans.append({'Tid': tag.Tid, 'Tname': tag.Tname})
        return Response({'tagList': ans})


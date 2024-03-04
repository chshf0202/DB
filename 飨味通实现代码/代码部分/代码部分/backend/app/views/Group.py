from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *


class GetAllGroup(APIView):
    def get(self, request):
        groupList = Group.objects.all().order_by('Gid')
        ans = []
        for group in groupList:
            ans.append({'Gid': group.Gid, 'Gname': group.Gname})
        return Response({'groupList': ans})


class AddGroup(APIView):
    GidBase = 0

    def post(self, request):
        ret = 0
        message = '添加菜品组成功'
        Gid = 'g' + str(AddGroup.GidBase).zfill(7)
        AddGroup.GidBase += 1
        Gname = request.data['Gname']
        if Group.objects.filter(Gname=Gname).exists():
            ret = 1
            message = '菜品组已注册'
            return Response({'value': ret, 'message': message})
        try:
            Group.objects.create(Gid=Gid, Gname=Gname)
        except Exception as e:
            print(e)
            ret = 2
            message = '添加菜品组失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})



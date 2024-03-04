from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *
from app.views.Picture import *


class GetDishComment(APIView):
    def post(self, request):
        Did = request.data['Did']
        ans = []
        try :
            dish = Dish.objects.get(Did=Did)
            commentList = Comment.objects.filter(Did=dish).order_by('Cid')
            for comment in commentList:
                PidList = CommentPicture.objects.filter(Cid=comment.Cid)
                user = User.objects.get(Uid=comment.Uid.Uid)
                if (user.Pid.Pid == 'p0000000'):
                    userPic = 'default.jpg'
                else:
                    userPic = Picture.objects.get(Pid=user.Pid.Pid).path
                pictureList = []
                for Pid in PidList:
                    picture = Picture.objects.get(Pid=Pid.Pid.Pid).path
                    pictureList.append(picture)
                ans.append({'Cid': comment.Cid, 'Uid': comment.Uid.Uid,
                            'pictureList': pictureList, 'content': comment.content,
                            'score': comment.score, 'userPic': userPic})
            return Response({'commentList': ans})
        except Dish.DoesNotExist:
            ret = 1
            message = '菜品未找到'
            return Response({'value': ret, 'message': message})
        except Picture.DoesNotExist:
            ret = 2
            message = '图片未找到'
            return Response({'value': ret, 'message': message})

class AddComment(APIView):
    CidBase = 0

    def post(self, request):
        ret = 0
        message = '评论成功'
        Cid = 'c' + str(AddComment.CidBase).zfill(7)
        AddComment.CidBase += 1
        Uid = request.data['Uid']
        Did = request.data['Did']
        content = request.data['content']
        score = request.data['score']
        pictureList = request.data['pictureList']
        try:
            user = User.objects.get(Uid=Uid)
            dish = Dish.objects.get(Did=Did)
            dishCommentNum = len(Comment.objects.filter(Did=dish))
            dish1 = Dish.objects.get(Did=dish.Did)
            dish1.score = (int(dish1.score) * dishCommentNum + int(score)) / (dishCommentNum + 1)
            dish1.save()
            comment = Comment.objects.create(Cid=Cid, Uid=user, Did=dish, content=content, score=score)
            comment.save()
            for picture in pictureList:
                Pid = getId()
                pic = Picture.objects.create(Pid=Pid, path=picture)
                pic.save()
                commentPicture = CommentPicture.objects.create(Cid=comment, Pid=pic)
                commentPicture.save()
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
            message = '上传评论图片失败'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})


class DeleteComment(APIView):
    def post(self, request):
        ret = 0
        message = '删除评论成功'
        Cid = request.data['Cid']
        try:
            comment = Comment.objects.get(Cid=Cid)
            comment.delete()
        except Comment.DoesNotExist:
            ret = 1
            message = '评价未找到'
            return Response({'value': ret, 'message': message})
        return Response({'value': ret, 'message': message})
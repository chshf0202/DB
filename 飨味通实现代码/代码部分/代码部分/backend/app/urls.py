# demo/urls.py

from django.urls import path
from app.views import Comment, Dish, Group, Order, Tag, User


app_name = "app"
urlpatterns = [
    #User
    path('AddUser/', User.AddUser.as_view()),
    path('LoginUserName/', User.LoginUserName.as_view()),
    path('LoginUserPhone/', User.LoginUserPhone.as_view()),
    path('UploadUserPicture/', User.UploadUserPicture.as_view()),
    path('ChangeUserPwd/', User.ChangeUserPwd.as_view()),
    path('ChangeUserUname/', User.ChangeUserUname.as_view()),
    path('ChangeUserPhone/', User.ChangeUserPhone.as_view()),
    path('UserStarDish/', User.StarDish.as_view()),
    path('UserUnstarDish/', User.UnstarDish.as_view()),
    path('GetStar/', User.GetStar.as_view()),
    path('GetUserInfo/', User.GetUserInfo.as_view()),

    #Dish
    path('GetDishDisplay/', Dish.GetDishDisplay.as_view()),
    path('GetDishWithTag/', Dish.GetDishWithTag.as_view()),
    path('AddDish/', Dish.AddDish.as_view()),
    path('AddDishRemain/', Dish.AddDishRemain.as_view()),
    path('AddDishTag/', Dish.AddDishTag.as_view()),
    path('GetUserOrderedDish/', Dish.GetUserOrderedDish.as_view()),

    #Group
    path('GetAllGroup/', Group.GetAllGroup.as_view()),
    path('AddGroup/', Group.AddGroup.as_view()),

    #Comment
    path('GetDishComment/', Comment.GetDishComment.as_view()),
    path('AddComment/', Comment.AddComment.as_view()),
    path('DeleteComment/', Comment.DeleteComment.as_view()),

    #Tag
    path('GetDishTag/', Tag.GetDishTag.as_view()),
    path('AddTag/', Tag.AddTag.as_view()),
    path('GetAllTag/', Tag.GetAllTag.as_view()),

    #Order
    path('GetUserOrder/', Order.GetUserOrder.as_view()),
    path('AddOrder/', Order.AddOrder.as_view()),

]

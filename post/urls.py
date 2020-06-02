from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# CBV viewset를 사용할 때는 router 만드는 것이 필요 ###############
router = DefaultRouter()
router.register('post', views.PostViewSet)
###########################################

urlpatterns = [
    path('fbv-test/', views.post_FBV),
    path('viewset/', include(router.urls)),

    path('api-view/', views.PostAPIView.as_view()),
    path('api-view/<int:post_id>', views.PostDetailApiView.as_view())
]

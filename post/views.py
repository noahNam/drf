"""
    FBV -> Function Based View
        -> view를 함수로 정의
    
    CBV -> Class Based View
        -> view를 클래스로 정의
"""
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from .permission import *
from .serializers import *
from .throttle import UserMinThrottle

"""
    FBV -> @api_view
    
    CBV -> APIView  : CRUD에 대해서 전부 직접 구현해야 
        -> mixin    : 필요한 기능을 상속받아서 간단하게 구현가능
        -> generics : CRUD에 대해서 custom이 조금 필요한 경우
        -> viewset  : CRUD에 대해서 custom이 필요하지 않은 경우
        
        상속관계 APIView > generics > viewset
"""

"""
    /post/
        -> GET -> post 리스트
        -> POST -> post 생성

    /post/{post_id}/
        -> GET -> post_id에 해당하는 post
        -> DELETE -> post_id에 해당하는 post 삭제
        -> UPDATE -> post_id에 해당하는 post 업데이트
"""

"""
    authentication_clases
        > TokenAuthentication
        > BasicAuthentication
        > SessionAuthentication
        > ..
        
    permission_classes
        > AllowAny
        > IsAuthenticated
        > IsAdminUser
        > IsAuthenticatedOrReadOnly
        > ..
    
    # Request 횟수 제한
    throttle_classes
        > AnonRateThrottle
        > UserRateThrottle
"""


class PostAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [ExampleAuthentication]
    # permission_classes = [PostPermission]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserMinThrottle]
    #throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        request.data['author'] = user.id

        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailApiView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs['post_id'])
        except Post.DoesNotExist:
            return Response({"description": "not found post"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs['post_id'])
        except Post.DoesNotExist:
            return Response({"description": "not found post"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs['post_id'])
        except Post.DoesNotExist:
            return Response({"description": "not found post"}, status=status.HTTP_404_NOT_FOUND)

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
@api_view(['GET', 'POST'])
def post_FBV(request):
    # post list를 반환
    if request.method == 'GET':
        posts = Post.objects.all()
        # serializing
        serializer = PostSerializer(posts, many=True)  # many : 여러 result를 가져올 때

        return Response(serializer.data, status=status.HTTP_200_OK)
    # post object 생성
    elif request.method == 'POST':
        # deserializing
        serializer = PostSerializer(data=request.data)

        # deserializing 저장할때는 항상 valid 해줘야함
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# viewset
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

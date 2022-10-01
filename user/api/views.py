from urllib import response
from django.urls import is_valid_path
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status ,viewsets, filters
from rest_framework.decorators import api_view , action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.authtoken.models import Token


class Users_list(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)

class User_list2(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    pagination_class=PageNumberPagination
    filter_backends=[filters.SearchFilter]
    search_fields=['username']
    authentication_classes=[TokenAuthentication]


class ProductList(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    pagination_class=PageNumberPagination
    filter_backends=[filters.SearchFilter]
    search_fields=['name']

@api_view(['GET'])
def find_products(request):
    products=Product.objects.filter(
        name=request.data['name']
    )
    serializer=ProductSerializer(products , many=True)
    return Response(serializer.data)


@api_view(['GET','POST'])
def usersjson3(request):
    if request.method == 'GET':
        users=User.objects.all()
        serializer=UserSerializer(users , many=True)
        return Response(serializer.data)

    elif request.method=='POST':
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def userjson3(request,id):
    try:
        user=User.objects.get(id=id)
    except user.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method== 'PUT':
        serializer=UserSerializer(user , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)

    if request.method=='DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CommentList(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    pagination_class=PageNumberPagination
    # authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self , request , *args , **kwargs):
        response={
            'message':'not-allowed'
        }
        return Response(response,status=status.HTTP_406_NOT_ACCEPTABLE)
    def update(self , request , *args , **kwargs):
        response={
            'message':'not-allowed'
        }
        return Response(response,status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def destroy(self , request , *args , **kwargs):
        response={
            'message':'not-allowed'
        }
        return Response(response,status=status.HTTP_406_NOT_ACCEPTABLE)
    
    @action(detail=True , methods=['GET'])
    def get_user_comments(self ,request,pk=None):
        product=Product.objects.get(id=pk)
        # username=request.data['username']
        # user=User.objects.get(username=username)
        user=request.user
        try:
            comments=Comment.objects.filter(user=user.id , product=product.id)
            serializer=CommentSerializer(comments , many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def updateComment(self,request,pk=None):
        product=Product.objects.get(id=pk)
        user=request.user
        # username=request.data['username']
        # user=User.objects.get(username=username)
        pro_comment=request.data['comment']
        rate=request.data['rate']

        try:
            #update
            comment=Comment.objects.filter(user=user ,product=product.id)
            comment.rate=rate
            comment.save()
            serializer=CommentSerializer(comment , many=True)
            json={
                'message':'Comment Updated',
                'result':serializer.data,
            }
            return Response(json , status=status.HTTP_200_OK)
        except:
            #create
            comment=Comment.objects.create(
                user=user,
                product=product,
                comment=pro_comment,
                rate=rate
            )
            serializer=CommentSerializer(comment)
            json={
                'message':'Comment Created',
                'result':serializer.data,
            }
            return Response(json , status=status.HTTP_200_OK)
            





class LoginView(viewsets.ModelViewSet):
    queryset=Token.objects.all()
    serializer_class=AuthTokenSerializer
    def create(self , request):
        return ObtainAuthToken().as_view()(request=request._request)




class RegisterApiView(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 



# Create your views here.
from django.shortcuts import render

import traceback
import logging
from django.db.utils import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .serializers import SerializerSignup, SerializerLogin

from .models import User, Product, ProductViews

from uuid import uuid4
import hashlib
from django.forms.models import model_to_dict


# from .serializers import SerializerTopTeamToWin
# from django.views.decorators.cache import cache_page


import csv
import json
# Create your views here.
log = logging.getLogger("debug")


class ProductView(APIView):
    '''
        '''
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        
        try:

            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
     
            try:
                user = User.objects.get(token=token)
            except:
                res = {'status': 'UNAUTHORIZED', "message": "wrong token"}
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

            
            product_id = request.GET.get('pid')

            if product_id:
                product_id = product_id
            else:
                res = {'status': 'FAILURE'}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

            try:
                product_id = int(product_id)
            except Exception as e:
                res = {'status': 'FAILURE'}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            
            print (product_id)
            product = Product.objects.get(productId=product_id)

            product_list = []
            
            if product:
                data = {}
                data['productId'] = product.productId
                data['productName'] = product.productName
                data['productImage'] = product.productImage
                data['salePrice'] = product.salePrice
                data['productPrice'] = product.productPrice
                data['productStock'] = product.productStock
                data['user_id'] = product.uid.uid
                data['productURL'] = request.build_absolute_uri().replace('/product/', '/p/?pid=')  +str(product.productId)
                data['modifiedTime'] = product.modified_time
                product_list.append(data)

                # to records views
                try:
                    product_view = ProductViews(productId = product, uid = user)
                    product_view.save()
                except Exception as e:
                    log.info("exception" + str(e) + str(x))
                

            res = {'status': 'SUCCESS'}
            res['data'] = product_list
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            x = traceback.format_exc()
            print (x)
            log.info("exception" + str(e) + str(x))
            res = {'status': 'FAILURE'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)




class ProductListView(APIView):
    '''
        '''
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        
        try:

            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
     
            try:
                user = User.objects.get(token=token)
            except:
                res = {'status': 'UNAUTHORIZED', "message": "wrong token"}
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

            products = Product.objects.all().order_by('-modified_time')

            product_list = []
            
            for product in products:
                data = {}
                data['productId'] = product.productId
                data['productName'] = product.productName
                data['productImage'] = product.productImage
                data['salePrice'] = product.salePrice
                data['productURL'] = request.build_absolute_uri().replace('/product-list/', '/product/?pid=')  +str(product.productId)
                data['modifiedTime'] = product.modified_time
                product_list.append(data)

            res = {'status': 'SUCCESS'}
            res['data'] = product_list
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            x = traceback.format_exc()
            print (x)
            log.info("exception" + str(e) + str(x))
            res = {'status': 'FAILURE'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)



    def post(self, request):
        
        try:

            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
     
            try:
                user = User.objects.get(token=token)
            except:
                res = {'status': 'UNAUTHORIZED', "message": "wrong token"}
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

            for product in request.data:

                try:
                    product_obj = Product(productId=product.get('productId'),
                    productCategory=product.get('productCategory'),
                    productName=product.get('productName'),
                    productImage=product.get('productImage'),
                    productStock=product.get('productStock'),
                    productPrice=product.get('productPrice'),
                    uid = user,
                    salePrice=product.get('salePrice')
                    )
                    product_obj.save()
                except Exception as e:

                    product_obj = Product.objects.get(productId=product.get('productId'))
                    product_obj.productId = product.get('productId')
                    product_obj.productCategory = product.get('productCategory')
                    product_obj.productName = product.get('productName')
                    product_obj.productImage = product.get('productImage')
                    product_obj.productStock = product.get('productStock')
                    product_obj.productPrice = product.get('productPrice')
                    product_obj.uid = user
                    product_obj.salePrice = product.get('salePrice')
                    product_obj.save()
                


            res = {'status': 'SUCCESS'}
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            x = traceback.format_exc()
            print (x)
            log.info("exception" + str(e) + str(x))
            res = {'status': 'FAILURE'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class AuthenticationSignup(APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        serlzr = SerializerSignup(data=request.data)

        if not serlzr.is_valid():
            res = {'status': 'FAILURE'}
            print ("vksjlskdg")
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        data = serlzr.data

        token = str(uuid4())


        password = data.get('password')
        password_hash = hashlib.sha1(password.encode('utf8')).hexdigest()

        try:
            user_obj = User(name=data.get('name'), email=data.get('email'), password=password_hash, token =token
                            )
            user_obj.save()


        except IntegrityError as e:
            log.info(e)
        
            res = {'status': 'FAILURE', 'message': "user already exit"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        user_dict = {"name": user_obj.name, "email": user_obj.email, "token": user_obj.token }

        res = {'status': 'SUCCESS', "token":user_obj.token}
        res.update(user_dict)
        return Response(res, status=status.HTTP_200_OK)



class AuthenticationLogin(APIView):

    renderer_classes = (JSONRenderer,)

    def post(self, request):

        try:
            serlzr = SerializerLogin(data = request.data)
            print (serlzr.is_valid())
            print(serlzr.data)

            if not serlzr.is_valid():
                res = {'status': 'FAILURE'}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

            data = serlzr.data

            try:
                user_obj = User.objects.get(email=data.get('email'))
                u_password_hash = user_obj.password
               
                if u_password_hash != hashlib.sha1(data.get('password').encode('utf8')).hexdigest():
                   
                    res = {'status': 'UNAUTHORIZED', "message": "wrong password"}
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist as e:
                log.info("user {} does not exist".format(str(data.get('email'))))
                res = {'status': 'FAILURE', 'message':"user does not exist"}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

            user_dict = {"name": user_obj.name, "email": user_obj.email}
            # print(request.GET['session'])
            res = {'status': 'SUCCESS', 'token': user_obj.token}
            res.update(user_dict)
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            x = traceback.format_exc()
            print (x)
            log.info("exception" + str(e) + str(x) )
            res = {'status': 'FAILURE'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)



class RecommendateProduct(APIView):
    '''
      
        '''
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        
        try:

            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
     
            try:
                user = User.objects.get(token=token)
            except:
                res = {'status': 'UNAUTHORIZED', "message": "wrong token"}
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

            
            friend_obj = User.objects.get(uid=2)
          
            product_view_obj = ProductViews.objects.filter(uid=friend_obj).values('productId').distinct()[:3]

            product_list = []
            
            for product in product_view_obj:

                product_id = product.get('productId')
                product = Product.objects.get(productId=product_id)

                data = {}
                data['productId'] = product.productId
                data['productName'] = product.productName
                data['productImage'] = product.productImage
                data['salePrice'] = product.salePrice
                data['productURL'] = request.build_absolute_uri().replace('/product-list/', '/product/?pid=')  +str(product.productId)
                data['modifiedTime'] = product.modified_time
                product_list.append(data)

                # to records views
                try:
                    product_view = ProductViews(productId = product, uid = user)
                    product_view.save()
                except Exception as e:
                    log.info("exception" + str(e) + str(x))
                

            res = {'status': 'SUCCESS'}
            res['data'] = product_list
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            x = traceback.format_exc()
            print (x)
            log.info("exception" + str(e) + str(x))
            res = {'status': 'FAILURE'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)



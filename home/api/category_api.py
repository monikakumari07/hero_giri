from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permission import *
from ..models import *
from .serializer import *
from dateutil.parser import parse
from datetime import datetime
class CategoryListCreate(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategoryCountSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#DELETE    
class CategoryListRetriveUpdateDelete(APIView):
    def delete(self,request,category_id):
        try:
            category = Category.objects.get(id=category_id) 
        except Category.DoesNotExist:
            return Response({"message": "Category Id not found"}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({"message": "Category Id deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#GET BY ID
    def get(Self,request,category_id):
        if category_id: 
            category_get = Category.objects.get(id=category_id)
            serializer = CategoryCountSerializer(category_get)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
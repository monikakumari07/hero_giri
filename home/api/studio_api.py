from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import IsSuperAdmin
from ..models import *
from .serializer import *
from dateutil.parser import parse
from datetime import datetime
from django.db import transaction

class StudioCreate(APIView):
    # permission_classes =[IsAuthenticated]
    def get(self, request):
        studio_get_all = Studio.objects.all()
        serializer = StudioSerializer(studio_get_all, many=True)
        print(serializer.data)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self,request):
        studio_name = request.data.get('studio_name')
        location = request.data.get('location')
        date_of_start = parse(request.data.get('date_of_start')).date()
        owner = request.data.get('owner')
        owner_number = request.data.get('owner_number')
        if not owner_number or not owner_number.isdigit():
            return Response({"message":"number should be Numerical"}, status=status.HTTP_400_BAD_REQUEST)
        if len(owner_number)!=10:
            return Response({"message":"number should be 10 digit"}, status=status.HTTP_400_BAD_REQUEST) 
        total_no_of_movies = request.data.get('total_no_of_movies')
        write_about_studio = request.data.get('write_about_studio')
        select_studio_type = request.data.get('select_studio_type')
        obj_studio = Studio.objects.filter(studio_name=studio_name).exists()
        if obj_studio:
            return Response({"message":"Already Register "},status=status.HTTP_400_BAD_REQUEST)
        
        studio = Studio.objects.create(
            studio_name=studio_name,
            location=location,
            date_of_start=date_of_start,
            owner=owner,
            owner_number=owner_number,
            total_no_of_movies=total_no_of_movies,
            write_about_studio=write_about_studio,
            select_studio_type=select_studio_type,
        )
        
        studio_pictures = request.FILES.getlist('studio_pictures', [])
        for pic in studio_pictures:
            obj_pictures = StudioPicture.objects.create(
                studio=studio,
                studio_picture=pic
            ) 
        

        studio_movie_pictures = request.FILES.getlist('studio_movie_pictures')
        for pic_data in studio_movie_pictures:
            movie_picture = StudioMoviePicture.objects.create(
                studio=studio,
                
                studio_movie=pic_data
            )
        studio.save()
        serializer = StudioSerializer(studio)
        return Response({"message":"sucessfully created","data":serializer.data},status=status.HTTP_201_CREATED )   

#UPDATE STUDIO
class StudioUpdateDelete(APIView):
    def put(self,request,studio_id):
        try:
            studio = Studio.objects.get(id=studio_id)
        except Studio.DoesNotExist:
            return Response({"message":"studio does not found"},status=status.HTTP_404_NOT_FOUND)
        
        obj_studio_name = Studio.objects.filter(studio_name=request.data.get('studio_name')).exists()
        if obj_studio_name:
            return Response({"message": "Studio name  already exist, please enter another name."}, status=status.HTTP_404_NOT_FOUND)
        studio.studio_name = request.data.get("studio_name", studio.studio_name)
        studio.location = request.data.get("location", studio.location)
        studio.date_of_start = parse(request.data.get("date_of_start", studio.date_of_start)).date()
        studio.owner = request.data.get("studio_name", studio.owner)
        studio.total_no_of_movies = request.data.get("total_no_of_movies", studio.total_no_of_movies)
        studio.write_about_studio = request.data.get("write_about_studio", studio.write_about_studio)
        studio.select_studio_type = request.data.get("select_studio_type", studio.select_studio_type)

# studio picture Updation         
        studio_pictures = request.FILES.getlist('studio_pictures', [])
        with transaction.atomic():
            studio.studio_picture.all().delete()
            for pic in studio_pictures:
                StudioPicture.objects.create(studio=studio, studio_picture=pic)

# studio movie picture Updation               
        studio_movie_pictures = request.FILES.getlist('studio_movie_pictures', [])
        with transaction.atomic():   # used to automtically create and delete the object
            studio.studio_movie.all().delete()
            for pic_data in studio_movie_pictures:
                StudioMoviePicture.objects.create(studio=studio, studio_movie=pic_data)

        studio.save()

        return Response({"message":"updated sucessfully", "status": status.HTTP_200_OK})


#DELETE
    def delete(self, request, studio_id):
        try:
            studio = Studio.objects.get(id=studio_id)
        except Studio.DoesNotExist:
            return Response({"message": "Studio Id not found"}, status=status.HTTP_404_NOT_FOUND)
        studio.delete()       
        return Response({"message": "Studio Id deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


#GET BY ID    
    def get(self, request,studio_id):
            if studio_id:
                get_by_studio = Studio.objects.get(id=studio_id)
                serializer = StudioSerializer(get_by_studio)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        

class StudioBookingCreate(APIView):
    # permission_classes =[IsAuthenticated,IsSuperAdmin]
    def post(self, request):            
        booking_studio = request.data.get('booking_studio', None)
        if booking_studio is None or booking_studio == '':       
            request.data['booking_studio'] = 'pending'      
        serializer =StudioBookingStatusSerializer(data=request.data)
        if serializer.is_valid():
            booking_studio = request.data.get('booking_studio', None)
            if booking_studio and booking_studio in ['accept', 'deny','pending']:              
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Invalid booking status value. Use 'accept', 'deny', 'pending'."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

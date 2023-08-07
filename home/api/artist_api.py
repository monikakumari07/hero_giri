from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import IsSuperAdmin
from .permission import *
from ..models import *
from .serializer import *
from dateutil.parser import parse
from datetime import datetime
from django.db import transaction
#ARTIST
class ArtistListCreateView(APIView):
    # permission_classes =[IsAuthenticated,IsSuperAdmin]
    def get(Self,request):
        artist_get_all = Artist.objects.all()
        serializer = ArtistSerializer(artist_get_all, many=True) #get all Artist data
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self,request):
        
        artist_name  = request.data.get('artist_name') 
        mobile_number  = request.data.get('mobile_number')
        if not mobile_number or not mobile_number.isdigit():
            return Response({"message":"mobile number should be Numerical"}, status=400)
        if len(mobile_number)!=10:
            return Response({"message":"mobile number should be 10 digit"}, status=400) 
        location  = request.data.get('location') 
        age  = request.data.get('age')       
        height  = request.data.get('height') 
        weight  = request.data.get('weight') 
        choose_acting_field = request.data.get('choose_acting_field')
        total_no_of_movies = request.data.get('total_no_of_movies')
        total_experience = request.data.get('total_experience')
        select_category = request.data.get('select_category')
        
        category_obj = Category.objects.get(category_name=select_category)
        existing_artist = Artist.objects.filter(mobile_number=mobile_number).exists()
        if existing_artist:
            return Response({"message": "You have already registered "}, status=status.HTTP_200_OK)
        user_obj = CustomUser.objects.create_user(username=mobile_number)
        if user_obj:
                            
            artist = Artist.objects.create(
                user=user_obj,
                artist_name=artist_name,
                mobile_number=mobile_number,
                location=location,
                age=age,
                height=height,
                weight=weight,    
                choose_acting_field=choose_acting_field, 
                total_no_of_movies=total_no_of_movies, 
                total_experience=total_experience, 
                select_category=category_obj,
                       
                )

            artist_pictures = request.FILES.getlist('artist_pictures',[])
            for picture in artist_pictures:
                pictures = ArtistPicture.objects.create(
                    artist=artist,
                    artist_picture=picture,                  
                )

            movie_pictures = request.FILES.getlist('movie_pictures')
            for picture_data in movie_pictures:
                picture = MoviePicture.objects.create(
                    artist=artist,
                    picture=picture_data,                  
                )
            artist.save()
            serializer = ArtistSerializer(artist)
            return Response({"message":"sucessfully created","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message":"OOPs Something went wrong"})

#Update
class ArtistListUpdate(APIView):
    def put(self,request,artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            return Response({"message": "artist not found"}, status=status.HTTP_404_NOT_FOUND)
        
        artist.artist_name = request.data.get('artist_name',artist.artist_name)
       
        existing_mobile_number = CustomUser.objects.filter(username=request.data.get("mobile_number")).exclude(id = artist.user.id)
        if existing_mobile_number:
            return Response({"message": "mobile  number already exist, please enter another number."}, status=status.HTTP_404_NOT_FOUND)
        
        artist.mobile_number = request.data.get('mobile_number',artist.mobile_number)

        artist.location = request.data.get('location',artist.location)
        artist.age = request.data.get('age',artist.age)
        artist.height = request.data.get('height',artist.height)
        artist.weight = request.data.get('weight',artist.weight)
        artist.choose_acting_field = request.data.get('choose_acting_field',artist.choose_acting_field)
        artist.total_no_of_movies = request.data.get('total_no_of_movies',artist.total_no_of_movies)
        artist.total_experience = request.data.get('total_experience',artist.total_experience)
       
#category updation        
        select_category_name = request.data.get('select_category')
        if select_category_name:
            try:
                category_obj = Category.objects.get(category_name=select_category_name)
                artist.select_category = category_obj
            except Category.DoesNotExist:
                return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
            
#artist picture Updation            
        artist_pictures = request.FILES.getlist('artist_pictures', [])
        artist.artist_pictures.all().delete()
        for pics in artist_pictures:
                ArtistPicture.objects.create(artist=artist, artist_picture=pics)

#artist movie picture Updation    
        movie_pictures = request.FILES.getlist('movie_pictures', [])
        print(movie_pictures)
        artist.movie_pictures.all().delete()
        for pic_movie in movie_pictures:
                MoviePicture.objects.create(artist=artist, picture=pic_movie)
    
        artist.save()
        user=artist.user
        if user:
           user.username = request.data.get("mobile_number")
           user.save()
        serializer = ArtistSerializer(artist)
        return Response({"message": "Successfully updated Artist details.", "data": serializer.data}, status=status.HTTP_200_OK)


#DELETE
    def delete(self,request,artist_id):
        try:
            artist = Artist.objects.get(id=artist_id) 
        except Artist.DoesNotExist:
             return Response({"message": "Artist Id not found"}, status=status.HTTP_404_NOT_FOUND)
        artist.delete()
        return Response({"message": "Artist Id deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#GET BY ID  
    def get(self, request,artist_id):
        if artist_id:
            artist_get_id = Artist.objects.get(id=artist_id)
            serializer = ArtistSerializer(artist_get_id)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        

#ARTIST BOOKING STATUS
class ArtistBookingAPI(APIView):
    # permission_classes =[IsAuthenticated,IsSuperAdmin]
    def post(self, request):     
        booking_status = request.data.get('booking_status', None)
        if booking_status is None or booking_status == '':            
            request.data['booking_status'] = 'pending' #set default to pending
        
        serializer =ArtistBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking_status = request.data.get('booking_status', None)
            if booking_status and booking_status in ['accepted', 'rejected', 'pending']:              
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Invalid booking status value. Use 'accepted', 'rejected', 'pending."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

















   

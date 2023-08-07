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

class AuditionCreate(APIView):
    # permission_classes =[IsAuthenticated,IsSuperAdmin]
    def get(self,request):
        audition_getall = Audition.objects.all()
        serializer = AuditionSerializer(audition_getall, many=True)
        print(serializer.data)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    def post(self, request):
        movie_poster = request.FILES['movie_poster']
        movie_name = request.data['movie_name']
        audition_date = parse(request.data['audition_date']).date()
        timings_from = request.data['timings_from']
        timings_to = request.data['timings_to']
        venue = request.data['venue']
        add_audition_position = request.data.getlist('add_audition_position') #list of selected positions
        story_line = request.data.get('story_line')
        existing_movie = Audition.objects.filter(movie_name=movie_name).exists()
        if existing_movie:
            return Response({"message": "You have already registered."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        audition = Audition.objects.create(
            movie_poster=movie_poster,
            movie_name=movie_name,
            audition_date=audition_date,
            timings_from=timings_from,
            timings_to=timings_to,  
            venue=venue,
            add_audition_position=add_audition_position, 
            story_line=story_line      
        )
        audition.save()
        serializer = AuditionSerializer(audition)
        return Response({"message": "Audition created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)

#UPDATE
class AuditionUpdateDelete(APIView):
   
    def put(Self,request,audition_id):
        try:
            audition_obj = Audition.objects.get(id=audition_id)
        except Audition.DoesNotExist:
            return Response({"message": "Audition Id not found",},status=status.HTTP_404_NOT_FOUND)
        audition_obj.movie_poster = request.data.get('movie_poster', audition_obj.movie_poster)
        
        existing_movie_name = Audition.objects.filter(movie_name=request.data.get('movie_name')).exists()
        if existing_movie_name:
            return Response({"message": "already exist enter another name."},
                            status=status.HTTP_400_BAD_REQUEST)
        audition_obj.movie_name = request.data.get('movie_name', audition_obj.movie_name)
        audition_obj.audition_date = parse(request.data.get('audition_date', audition_obj.audition_date)).date()
        audition_obj.timings_from = request.data.get('timings_from', audition_obj.timings_from)
        audition_obj.timings_to = request.data.get('timings_to', audition_obj.timings_to)
        audition_obj.venue = request.data.get('venue',audition_obj.venue)
        audition_obj.add_audition_position = request.data.get('add_audition_position', audition_obj.add_audition_position)
        audition_obj.story_line = request.data.get('story_line',audition_obj.story_line)
        audition_obj.save()
        return Response({"message":"updated sucessfully", "status": status.HTTP_200_OK})

#DELETE
    def delete(self,request,audition_id):
        try:
            audition = Audition.objects.get(id=audition_id)
            print(audition_id)
        except Audition.DoesNotExist:
            return Response({"message":"Audition Id not exist"},status=status.HTTP_400_BAD_REQUEST)
        audition.delete()
        return Response({"message": "Audition deleted successfully"}, status=status.HTTP_200_OK)    

#get by id
    def get(self,request,audition_id):
        if audition_id:
            get_by_audition = Audition.objects.get(id=audition_id)
            serializer = AuditionSerializer(get_by_audition)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
#REQUEST AUDITION API
class RequestAuditionApi(APIView):
    def post(self, request, format=None):
        artist = Artist.objects.get(user=request.user)      
        print(artist)
        applied_date = request.data['applied_date']
        selection_status = request.data['selection_status']
        if not selection_status.strip():  
            selection_status = 'pending'  

        print(selection_status)
        audition_id = request.data['audition']
        print(audition_id)
        try:
            exist_audition = Audition.objects.get(id=audition_id)
        except Audition.DoesNotExist:
            return Response({"message": "Audition Id not found"}, status=status.HTTP_404_NOT_FOUND)
        request_audition = RequestAudition.objects.create(
            artist=artist,
            applied_date=applied_date,
            selection_status=selection_status,
            audition_id=audition_id
        )
        request_audition.save()
        
        return Response({"message": "Request send  successfully."}, status=status.HTTP_201_CREATED)

#REQUEST AUDITION UPDATE API        
class GetPendingRequestAudition(APIView): 
    # permission_classes = [IsAuthenticated,IsSuperAdmin]
    def patch(self, request, format=None):              
        data = request.data.get('data', [])  
        selection_status = request.data.get('selection_status', 'pending') 

        if not data:
            return Response({"message": "No data found in the request."}, status=status.HTTP_400_BAD_REQUEST)

        for item in data:
            request_id = item.get('request_id')
            artist_id = item.get('artist_id')

            if request_id is None or artist_id is None:
                return Response({"message": "Each item in 'data' must contain 'request_id' and 'artist_id'."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                request_audition = RequestAudition.objects.get(id=request_id, artist=artist_id)
            except RequestAudition.DoesNotExist:
                return Response({"message": f"Request Audition not found for artist {artist_id} and request {request_id}."}, status=status.HTTP_404_NOT_FOUND)

            if selection_status not in ['pending', 'accepted', 'rejected']:
                return Response({"message": "Invalid selection status. Use 'pending', 'accepted', or 'rejected'."}, status=status.HTTP_400_BAD_REQUEST)

            request_audition.selection_status = selection_status
            request_audition.save()

        return Response({"message": "Selection status updated successfully."}, status=status.HTTP_200_OK)

      
#GET AUDITION REQUEST
    def get(self,request):                    
        try:
            artist = Artist.objects.get(user=request.user)
            print(artist)
            obj_pending = RequestAudition.objects.filter(selection_status='pending', artist=artist)
            serializer = RequestAuditionSerializer(obj_pending, many=True)
            return Response({"message": "OK", "data": serializer.data}, status=status.HTTP_200_OK)
        except Artist.DoesNotExist:
            return Response({"message": "Artist not found for the current user"}, status=status.HTTP_404_NOT_FOUND)
        except RequestAudition.DoesNotExist:
            return Response({"message": "RequestAudition not found for the given audition_id"}, status=status.HTTP_404_NOT_FOUND)
        
       

#SIDEBAR API start
#FAQ
class FAQListView(APIView):
    def get(self,request):
        faq = FAQ.objects.all()
        serializer = FAQSerializer(faq,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FAQAnswerView(APIView):
    def get(Self,request,id):
        try:
            obj_faq = FAQ.objects.get(id=id)
            serializer = FAQAnswereSerializer(obj_faq)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FAQ.DoesNotExist:
            return Response(
                {"detail": "FAQ not found."},
                status=status.HTTP_404_NOT_FOUND
            )

class ContactHelpDetails(APIView):
    def get(self,request,format=None):
        contact_help = ContactHelp.objects.all()
        serializer = ContactHelpSerializer(contact_help, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PrivacyPolicyApiview(APIView):
    def get(self,request):
        privacy_policies = PrivacyPolicy.objects.all()
        serializer = PrivacyPolicySerializer(privacy_policies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

class AboutUsApiview(APIView):
    def get(self,request):
        about_us = AboutUs.objects.all()
        serializer = AboutUsSerializer(about_us, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

#END SIDEBAR API




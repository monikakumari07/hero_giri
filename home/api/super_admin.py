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

class CampaignsCreateApi(APIView):
    permission_classes =[IsAuthenticated]
    def get(self, request):
        campaigns_get_all = Campaigns.objects.all()
        serializer = CampaignsSerializer(campaigns_get_all, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self,request):       
        campaigns_name  = request.data.get('campaigns_name') 
        genere  = request.data.get('genere') 
        appx_budget  = request.data.get('appx_budget')       
        movie_start_date = request.data.get('movie_start_date')
        movie_start_end = request.data.get('movie_start_end')
        audition_date = request.data.get('audition_date')
        donation_return = request.data.get('donation_return')
        one_line_story  = request.data.get('one_line_story')
        movie_poster = request.FILES.get('movie_poster')
        actors_data = request.data.get('actors_list', [])
        actors_instances = []

        existing_campaign = Campaigns.objects.filter(campaigns_name=campaigns_name).exists()
        if existing_campaign:
            return Response({"message": "You have already registered a campaign."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        campaign = Campaigns.objects.create(
            # user=user,
            campaigns_name=campaigns_name,
            genere=genere,
            appx_budget=appx_budget,
            movie_start_date=movie_start_date,
            movie_start_end=movie_start_end,
            audition_date=audition_date,
            one_line_story=one_line_story,
            donation_return=donation_return,
            movie_poster=movie_poster,						
            )        
        for actor_data in actors_data:
            actor_id = actor_data.get('id')    
                           
            try:
                actor = Actors.objects.get(id=actor_id)
                print(actor)
                campaign.actors.add(actor) #Add multiple actors             
            except Actors.DoesNotExist:
                return Response({"error": "Actor with ID {actor_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        campaign.save()

        serializer = CampaignsSerializer(campaign)
        return Response({"message":"sucessfully created","data":serializer.data}, status=status.HTTP_201_CREATED)
    
#UPDATE Campaign    
class CampaignsUpdate(APIView):
    permission_classes =[IsAuthenticated]
    def put(self, request, campaign_id):
        try:
            campaign = Campaigns.objects.get(id=campaign_id)
        except Campaigns.DoesNotExist:
            return Response({"error": "Campaign not found or you don't have permission to update it."},
                            status=status.HTTP_404_NOT_FOUND)
        obj_campaigns_name = Campaigns.objects.filter(campaigns_name=request.data.get('campaigns_name')).exists()
        if obj_campaigns_name:
            return Response({"message": "Campaigns name  already exist, please enter another name."}, status=status.HTTP_404_NOT_FOUND)
        
        campaign.campaigns_name = request.data.get("campaigns_name", campaign.campaigns_name)
        campaign.genere = request.data.get("genere", campaign.genere)
        campaign.appx_budget = request.data.get("appx_budget", campaign.appx_budget)
        campaign.movie_start_date = request.data.get("movie_start_date", campaign.movie_start_date)
        campaign.audition_date = request.data.get("audition_date", campaign.audition_date)
        campaign.one_line_story = request.data.get("one_line_story", campaign.one_line_story)
        campaign.donation_return = request.data.get("donation_return", campaign.donation_return)
        campaign.movie_poster = request.data.get("movie_poster", campaign.movie_poster)
        campaign.save()

        return Response({"message":"updated sucessfully", "status": status.HTTP_200_OK})
    
    #delete 
    def delete(self, request, campaign_id):
        try:
            campaign = Campaigns.objects.get(id=campaign_id)
        except Campaigns.DoesNotExist:
            return Response({"message": "Campaigns Id not found"}, status=status.HTTP_404_NOT_FOUND)
        campaign.delete()
        return Response({"message": "Campaigns Id deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    #GET BY ID
    def get(self, request,campaign_id):
        if campaign_id:
            campaign_get_id = Campaigns.objects.get(id=campaign_id)
            serializer = CampaignsSerializer(campaign_get_id)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
         

class ActorsApi(APIView):
    def post(self, request):
        name = request.data.get('name')
        profile = request.FILES.get('profile')
        
        actor = Actors.objects.create(name=name, profile=profile)
        serializer = ActorsSerializer(actor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#UPDATE Actor
class ActorsUpdateApi(APIView):
    def put(self, request, actor_id):
        try:
            actor = Actors.objects.get(id=actor_id)
        except Actors.DoesNotExist:
            return Response({"error": "Actor not found."},
                            status=status.HTTP_404_NOT_FOUND)       
        serializer = ActorsSerializer(actor, data=request.data, partial=True)# Use the update serializer for updating the actor
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully updated", "data": serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from django.urls import path, include
from rest_framework import routers
from .super_admin import *
from .user_api import *
from .artist_api import *
from .studio_api import *
from .audition_api import *
from .category_api import *

router = routers.DefaultRouter()
urlpatterns=[
    path('', include(router.urls)),
    #SUPERUSER APIS
    path('user-details/', UserDetailAPI.as_view(), name='user-details'),
    path('user-details-update/<int:userdetails_id>/', UserDetailUpdateAPI.as_view(), name='user-details-update'),
    path('user-genrate-otp/', GenrateOtpMobile.as_view(), name='user-register'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('actor/', ActorsApi.as_view(), name='actor'),
    path('actors-update/<int:actor_id>/', ActorsUpdateApi.as_view(), name='actors-update'),
    path('campaign-create/', CampaignsCreateApi.as_view(), name='actor'),
    path('campaign-update/<int:campaign_id>/', CampaignsUpdate.as_view(), name='campaign-update'),
    path('artistlist-create/', ArtistListCreateView.as_view(), name='actor'),
    path('artistlist-update/<int:artist_id>/', ArtistListUpdate.as_view(), name='artistlist-get-by-id'),
    path('artist-booking/', ArtistBookingAPI.as_view(), name='artist-booking'),



    #USER LOGIN
    path('user-login/', UserLogin.as_view(), name='user-register'),
    path('otp-login-verify/', OTPLoginVerify.as_view(), name='user-register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    
    #STUDIO APIs
    path('studio-create/',StudioCreate.as_view(), name='studio-create'),
    path('studio-update-delete/<int:studio_id>/', StudioUpdateDelete.as_view(), name='studio-update-delete'),
    path('studio-booking-status/',StudioBookingCreate.as_view(), name='studio-booking-status'),

    #CATEGORY
    path('category/', CategoryListCreate.as_view(), name='category-list-create'),
    path('category-delete/<int:category_id>/', CategoryListRetriveUpdateDelete.as_view(), name='category-list-create'),
    #AUDITION
    path('audition-create/',AuditionCreate.as_view(), name='audition-create'),
    path('audition-update-delete/<int:audition_id>/',AuditionUpdateDelete.as_view(), name='audition-create'),
    path('request-audition/',RequestAuditionApi.as_view(), name='request-audition'),
    path('get-pending-requests/',GetPendingRequestAudition.as_view(), name='get-pending-requests'),
   
    #FAQ
    path('faq/',FAQListView.as_view(), name='faq'),
    path('faq-answer/<int:id>/',FAQAnswerView.as_view(), name='faq-answer'),
    path('contact-help/',ContactHelpDetails.as_view(), name='contact-help'),
    path('privacy-policy/',PrivacyPolicyApiview.as_view(), name='privacy-policy'),
    path('aboutus/',AboutUsApiview.as_view(), name='aboutus'),
]
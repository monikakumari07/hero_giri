from ..models import *
from rest_framework import serializers
from django.core.exceptions import ValidationError
from dateutil.parser import parse

class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['otp']
		
class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserDetail
		fields = "__all__"

class ActorsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Actors
		fields = ('id', 'name', 'profile')


class CampaignsSerializer(serializers.ModelSerializer):
	actors = ActorsSerializer(many=True)
	class Meta:
		model = Campaigns
		fields = "__all__"

class CampaignsUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Campaigns
		fields = ['campaigns_name', 'genere', 'appx_budget', 'movie_start_date',
				  'movie_start_end', 'audition_date', 'donation_return',
				  'one_line_story', 'movie_poster']


class MoviePictureSerializer(serializers.ModelSerializer):
	class Meta:
		model = MoviePicture
		fields = '__all__'
	

class UpdatedMoviePictureSerializer(serializers.ModelSerializer):
	class Meta:
		model = MoviePicture
		fields = ['picture']

class  ArtistPictureSerializer(serializers.ModelSerializer):
	class Meta:
		model = ArtistPicture
		fields = ['artist_picture']
	

class ArtistSerializer(serializers.ModelSerializer):
    movie_pictures = UpdatedMoviePictureSerializer(many=True, read_only=True)
    artist_pictures = ArtistPictureSerializer(many=True, read_only=True)
    select_category = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = '__all__'

    def get_select_category(self, obj):
        return str(obj.select_category)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['select_category'] = data['select_category'].split('of')[0].strip()
        return data    
    

class ArtistMovieSerializer(serializers.ModelSerializer):
	class Meta:
		
		model =MoviePicture
		fields = '__all__'


class ArtistBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistBooking
        fields = ['artist','booking_status','booking_date']

class StudioPictureSerializer(serializers.ModelSerializer):
	class Meta:
		model = StudioPicture
		fields = '__all__'

class StudioMoviePictureSerializer(serializers.ModelSerializer):
	class Meta:
		model = StudioMoviePicture
		fields = '__all__'

class StudioSerializer(serializers.ModelSerializer):
	studio_picture = StudioPictureSerializer(many=True, read_only=True)  # Nested serializer for studio_pictures
	studio_movie = StudioMoviePictureSerializer(many=True, read_only=True)  # Nested serializer for studio_movie_pictures

	class Meta:
		model = Studio
		fields = '__all__'

class StudioBookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioBooking
        fields = '__all__'

    def calculate_no_of_days(self, from_date, to_date):
        if from_date and to_date:
            delta = to_date - from_date # Calculate no_of_days 
            return delta.days
        return None

    def create(self, validated_data):
        from_date = (validated_data.get('from_date', None))
        to_date = (validated_data.get('to_date', None))   
        no_of_days = self.calculate_no_of_days(from_date, to_date) 
        validated_data['no_of_days'] = no_of_days

        return super().create(validated_data)

class  AuditionSerializer(serializers.ModelSerializer):
	class Meta:
		model =  Audition
		fields = '__all__'

		
class RequestAuditionSerializer(serializers.ModelSerializer):
	artist = ArtistSerializer()
	class Meta:
		model = RequestAudition
		fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'
		
class CategoryCountSerializer(serializers.ModelSerializer):
    total_members = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'total_members']

    def get_total_members(self, obj):
        artists = obj.artists.all()  # Get all the artists associated with the category
        serializer = ArtistSerializer(artists, many=True)
        return {
            'count': artists.count(),
            'details': serializer.data
        }	


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('id','question',)

class FAQAnswereSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('answer',)

class ContactHelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactHelp
        fields = ['id', 'email', 'helpline_number']

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'
		
class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'
		


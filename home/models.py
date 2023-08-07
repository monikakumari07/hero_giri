from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import datetime

class CustomUser(AbstractUser):
    otp = models.CharField(max_length=6,blank=True,null=True)
    is_user = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)

    def __str__(self):
        if self.username:
            return self.username
        elif self.email:
            return self.email
        else:
            return f"User {self.id}"
class Otp(models.Model):
    mobile_number = models.CharField(max_length=12)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return str(self.otp)
    

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    def __str__(self):
        return self.category_name 


class UserDetail(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=12)
    city = models.CharField(max_length=12)
    pin_code = models.CharField(max_length=6)
    profile = models.FileField(upload_to='register/docs')

    def __str__(self):
        return str(self.user.username) 
    
#Actor model    
class Actors(models.Model):
    name = models.CharField(max_length=100)
    profile = models.FileField(upload_to='actor/docs')

    def __str__(self):
        return self.name
    
#Campaigns
class Campaigns(models.Model):
    actors = models.ManyToManyField(Actors)
    campaigns_name = models.CharField(max_length=20)
    genere = models.CharField(max_length=25)
    appx_budget = models.DecimalField(max_digits=10, decimal_places=2)
    movie_start_date = models.DateField()
    movie_start_end = models.DateField()
    audition_date = models.DateField()
    donation_return = models.DateField()
    one_line_story = models.TextField()
    movie_poster = models.FileField(upload_to='campaigns/docs')
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    
    def __str__(self):
        return self.campaigns_name
    
#ARTIST 
class Artist(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE) #user is associated with each artist 
    artist_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=12)
    location = models.CharField(max_length=25)
    age = models.PositiveIntegerField()
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    ACTING_FIELD = (
        ('movies', 'Movies'),
        ('serials', 'Serials')
    )
    choose_acting_field = models.CharField(max_length=100, choices=ACTING_FIELD,blank=True,null=True)
    total_no_of_movies = models.PositiveIntegerField()
    total_experience = models.CharField(max_length=100)
    select_category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name='artists' )
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return f"{self.artist_name} - {self.select_category.category_name}"


class ArtistPicture(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_pictures')
    artist_picture = models.FileField(upload_to='artist/docs')
    def __str__(self):
        return f"Artist_Picture {self.id}"

class ArtistBooking(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_booking')
    booking_date = models.DateField(auto_now_add=True,null=True, blank=True)
    STATUS_CHOICES = (
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending')
    )
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.booking_status} - {self.id}"
#Artist MODEL END    

#Studio
class Studio(models.Model):
    studio_name = models.CharField(max_length=50)
    location =  models.CharField(max_length=50)
    date_of_start = models.DateField()
    owner = models.CharField(max_length=20)
    owner_number = models.CharField(max_length=12)
    total_no_of_movies = models.PositiveIntegerField()
    write_about_studio = models.TextField()
    STUDIO_TYPE = (
        ('editing/dubbing','Editing/Dubbing'),
        ('music recording','Music Recording'),
        ('house location','House Location')        
    )
    select_studio_type = models.CharField(max_length=50, choices=STUDIO_TYPE)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return f"{self.studio_name} - {self.id}"
    
class StudioPicture(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='studio_picture')
    studio_picture = models.FileField(upload_to='studio/docs')
    def __str__(self):
        return f"Studio_Picture {self.id}"
   
class MoviePicture(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='movie_pictures')
    picture = models.FileField(upload_to='movie/docs')
    def __str__(self):
        return f"Picture {self.id}"


class StudioMoviePicture(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='studio_movie')
    studio_movie = models.FileField(upload_to='movies/docs')
    def __str__(self):
        return f"Picture {self.id}"
    

class StudioBooking(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='studio_booking')
    studio_booking_date = models.DateField(auto_now_add=True,null=True, blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    no_of_days = models.PositiveIntegerField(null=True,blank=True)
    BOOKING_TYPE=(
        ('accept','Accept'),
        ('deny','Deny'),
        ('pending','Pending'),
    )
    booking_studio = models.CharField(max_length=50, choices=BOOKING_TYPE, default='pending')

    def __str__(self):
        return f"{self.booking_studio} - {self.id}"


class Audition(models.Model):
    movie_poster = models.FileField(upload_to='movieposter/docs')
    movie_name = models.CharField(max_length=20)
    audition_date = models.DateField()
    timings_from = models.TimeField()
    timings_to = models.TimeField()
    venue = models.TextField()
    POSITION_CHOICES = (
        ('hero', 'Hero'),
        ('herione', 'Herione'),
        ('supporting role', 'Supporting Role'),
        ('villain', 'Villain'),
        ('musician', 'Musician'),        
    )
    add_audition_position = models.CharField(max_length=300)
    story_line = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    

    def __str__(self):
        return f"{self.movie_name} - {self.id}"

class RequestAudition(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='request')
    audition = models.ForeignKey(Audition, on_delete=models.CASCADE, related_name='request')
    applied_date = models.DateTimeField(auto_now_add=True)
    SELECTION_LIST = (
        ('selected', 'Selected'),
        ('rejected','Rejected'),
        ('pending', 'Pending')
    )
    selection_status = models.CharField(max_length=20, choices=SELECTION_LIST, default='pending')
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return self.selection_status
    
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.question

class ContactHelp(models.Model):
    helpline_number = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.helpline_number 

class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title 

class AboutUs(models.Model):
    aboutus_title = models.CharField(max_length=100)
    aboutus_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.aboutus_title


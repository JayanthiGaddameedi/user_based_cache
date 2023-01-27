# user_based_cache

##### packages

1. django
2. django-redis
3. redis
4. django rest framework
5. django rest_framework_simplejwt

##### Get started

1. Install all the requirements - `pip install -r requirements.txt`
2. In settings.py add the following lines.
    1. ```
       Installed_apps = [
           'rest_framework',
           'rest_framework_simplejwt',
       ]
       ```
    2. Add the simplejwt in settings.py file
       ```
       REST_FRAMEWORK = {
          'DEFAULT_AUTHENTICATION_CLASSES': [
               'rest_framework_simplejwt.authentication.JWTAuthentication',
           ],
       }
       ```
    3. Add these cache lines in settings.py
       ``` 
       CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
             },
            "KEY_PREFIX": "user_based_cache"
           }
       }
       
       #  Cache time to live is 15 minutes
       CACHE_TTL = 60 * 15
       ```
3. models.py
    ```
   from django.contrib.auth.models import AbstractUser

   class CustomUser(AbstractUser): 
        phone_number = models.IntegerField(null=True, blank=True)
   
   class Newsfeed(models.Model):
        news = models.CharField(max_length=255)
   ```
4. As we are using Django’s built -in class AbstractUser, we need to add this user model to our settings.py file.
    ```
   AUTH_USER_MODEL = 'datarepo.CustomUser'  # datarepo is the app_name(app_name.model_name)
   ```
5. admin.py
   ```
   from django.contrib.auth.admin import UserAdmin
   from .models import Newsfeed
   
   class CustomUserAdmin(UserAdmin):
       list_display = ('id', 'phone_number')

   UserAdmin.fieldsets += (
        (
            'custom_fields', {
                'fields': ('phone_number',)
            }
        ),
   )
    
   admin.site.register(CustomUser, CustomUserAdmin)
       
   @admin.register(Newsfeed)
   class NewsfeedAdmin(admin.ModelAdmin): 
       list_display = ('id', 'news')

   ```
6. views.py

    ```
   import random
   from django.conf import settings
   from django.views.decorators.vary import vary_on_headers
   from rest_framework.decorators import api_view, authentication_classes, permission_classes
   from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
   from rest_framework.permissions import IsAuthenticated
   from rest_framework import status
   from rest_framework.response import Response
   from django.views.decorators.cache import cache_page
   from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
   
   from .models import Newsfeed, CustomUser

    
   @api_view(['GET'])
   @authentication_classes([JWTTokenUserAuthentication])
   @permission_classes([IsAuthenticated])
   @cache_page(settings.CACHE_TTL)
   @vary_on_headers('Authorization', )
   def list_newsfeed(request):
       all_newsfeed = Newsfeed.objects.filter(user_id=request.user.id)
       data = [] 
       for item in all_newsfeeds:
           temp = {
               'news_id': item.id,
               'user_id': item.user_id,
               'news': item.news
           }
           data.append(temp)
       context = {'test': random.randint(100, 999), 'data': data} 
       return Response(context, status=status.HTTP_200_OK)

    ```
7. urls.py
   ```
   from datarepo.views import list_newsfeed
   
    urlpatterns = [
        path('list_newsfeed/', list_newsfeed)
    ]
   ```
8. To check redis connected
   ```
   $ redis-cli ping
   PONG
   ```
9. To test redis is working fine..!!
   ```
    $ redis-cli
    127.0.0.1:6379> set test "hello world"
    127.0.0.1:6379> OK
    127.0.0.1:6379> get test
    127.0.0.1:6379> "hello world"
    ```
10. To know the cache keys
     ```
    $ python3 manage.py shell
      >>> from django.core.cache import cache
      >>> cache.keys('*')  # this line gives the list of keys presenet in cache

    ```
11. To clear the cache
    ```
    >>> from django.core.cache import cache
    >>> cache.clear()
       True
    ```

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from watchlist_app.api import serializers
from watchlist_app import models

# class RegisterTestCase(APITestCase):
#     def test_register(self):
#         data = {
#             'username': 'testcase',
#             'email': 'testcase@gmail.com',
#             'password': '12345678',
#             'password2': '12345678'
#         }
#         response = self.client.post(reverse('register'), data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# class LoginLogoutTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testcase', password='12345678')

#     def test_login(self):
#         data = {
#             'username': 'testcase',
#             'password': '12345678',
#         }
#         response = self.client.post(reverse('login'), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_logout(self):
#         self.token, _ = Token.objects.get_or_create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         response = self.client.post(reverse('logout'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class StreamPlatformTestCase(APITestCase):
#     def setUp(self):
#         self.user=User.objects.create(username='testuser', password='12345678')
#         self.token, _ =Token.objects.get_or_create(user__username=self.user.username)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) #same effect of login
        
#     def test_stream_platform_create(self):
#         data={
#             'name':'netflix',
#             'about':'top streaming platform',
#             'website':'https://netflix.com'
#         }
#         response=self.client.post(reverse('stream-platform-list'),data)
#         self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
            
        
class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='12345678')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) # same effect as login
        #sample item is created for testing list and individual item
        self.stream=models.StreamPlatform.objects.create(name='netflix',about='top streaming platform',website='https://netflix.com')
        
        
    def test_stream_platform_create(self):
        data = {
            'name': 'netflix',
            'about': 'top streaming platform',
            'website': 'https://netflix.com'
        }
        response = self.client.post(reverse('stream-platform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)#normal users are forbidden from creating stream platform        
    
    def test_stream_platform_list(self):
        response = self.client.get(reverse('stream-platform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_stream_platform_individual(self):
        response = self.client.get(reverse('stream-platform-list-detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        
    #also methods for put and delete,only admin is able to do this     
    
    
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='12345678')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) # same effect as login
        #sample item is created for testing list and individual item
        #to add a watchlist a platform is required
        self.stream=models.StreamPlatform.objects.create(name='netflix',about='top streaming platform',website='https://netflix.com')
        self.watchlist=models.WatchList.objects.create(platform=self.stream,title='Angular',storyline='nice movie',active=True)
        
    
    def test_watchlist_create(self):
        data = {
            'platform': self.stream,
            'title': 'Angular',
            'storyline': 'nice movie',
            'active':True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)#normal users are forbidden from creating watchlist 
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_individual(self):
        response = self.client.get(reverse('movie-detail',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='12345678')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) # same effect as login
        #sample item is created for testing list and individual item
        #to add a watchlist a platform is required
        self.stream=models.StreamPlatform.objects.create(name='netflix',about='top streaming platform',website='https://netflix.com')
        self.watchlist=models.WatchList.objects.create(platform=self.stream,title='Angular',storyline='nice movie',active=True)
        self.watchlist2=models.WatchList.objects.create(platform=self.stream,title='React',storyline='bad movie',active=True)

        self.review=models.Review.objects.create(review_user=self.user,rating=5,description='super movie',watchlist=self.watchlist2,active=True)
        
        
    def test_review_create(self):
        data={
            'review_user':self.user,
            'rating':5,
            'description':'super movie',
            "watchlist":self.watchlist,
            "active":True
            
        }
        response = self.client.post(reverse('watch_list-review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)    

    #unauthorized user tries to create a review
    def test_review_create_unauth(self):
        data={
            'review_user':self.user,
            'rating':5,
            'description':'super movie',
            "watchlist":self.watchlist,
            "active":True
            
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('watch_list-review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   
        
    def review_update(self):
        data={
            'review_user':self.user,
            'rating':4,
            'description':'super movie updated',
            "watchlist":self.watchlist,
            "active":False
            
        }
        response = self.client.put(reverse('review-detail',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

    def test_review_list(self):
        response = self.client.get(reverse('review-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_review_detail(self):
        response = self.client.get(reverse('review-detail',args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
                 
    #similarly delete request    
    
    #test for user getting his own reviews
    def test_review_user(self):
        response = self.client.get('/api/user_review_detail/?username'+self.user.username)  #data passed in params
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
              
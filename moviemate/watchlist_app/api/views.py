from urllib import response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from watchlist_app.api.pagination import WatchListCursorPagination, WatchListLimitOffsetPagination, WatchListPagination
from watchlist_app.api.permissions import AdminOrReadOnly,IsAuthorOrReadOnly
# from watchlist_app.models import Movie,
from watchlist_app.models import Review, WatchList,StreamPlatform
# from watchlist_app.api.serializers import MovieSerializer,WatchListSerializer
from watchlist_app.api.serializers import ReviewSerializer, ReviewSerializerForSpecificCreate, WatchListSerializer,StreamPlatformSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottling,ReviewListThrottling

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

#to get all the reviews submitted by specific user
class UserReview(generics.ListAPIView):
    serializer_class=ReviewSerializer
    
    #common method of overriding builtin method get_queryset in case of filtering condition is passed in url
    def get_queryset(self):
        username=self.kwargs['username']
        return Review.objects.filter(review_user__username=username) 
    
    #common method of overriding builtin method get_queryset in case of filtering condition is passed in params
    def get_queryset(self):
        username=self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username) 








# StreamPlatformViewSet with modelviewset concept
#no need for overriding list create retrieve update destroy methods
#all will be automatically taken
class StreamPlatformViewSet(viewsets.ModelViewSet):
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializer
    permission_classes=[AdminOrReadOnly]#only admin can edit
    
    
#if we need to remove post,put,delete request that is create,update,destroy method from this class we can inherit Readonlymodelviewset   
#it only allows get request for list and retreive methods 
# class StreamPlatformViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset=StreamPlatform.objects.all()
#     serializer_class=StreamPlatformSerializer    

# # class based view with the concept of viewset
# #we have to override list retrieve create update destroy
# #all operations is like a set in a class
# class StreamPlatformViewSet(viewsets.ViewSet):
    
#     def list(self, request):
#         stream_platforms=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(stream_platforms,many=True)
#         return Response(serializer.data)
    
    
#     def retrieve(self, request,pk=None):
#         queryset=StreamPlatform.objects.all()
#         stream_platform=get_object_or_404(queryset,pk=pk)
#         serializer=StreamPlatformSerializer(stream_platform)
#         return Response(serializer.data)
    
#     def create(self,request):
#         stream_platform_serializer = StreamPlatformSerializer(data=request.data)
#         if stream_platform_serializer.is_valid():
#             stream_platform_serializer.save()
#             return Response(stream_platform_serializer.data,status=status.HTTP_201_CREATED)
#         else:
#              return Response(stream_platform_serializer.errors) 
         
#         #update destroy methods can also be given  
        


#concrete class based view
#this will create review specific to a movie
class WatchListSpecificReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializerForSpecificCreate
    queryset=Review.objects.all()
    permission_classes=[IsAuthenticated]
    #customized thottling for this view only
    throttle_classes =[ReviewCreateThrottling]
    
    def perform_create(self, serializer):
        watchlist_id=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=watchlist_id)
        print(watchlist)
        review_user=self.request.user
        print(review_user)
        query=Review.objects.filter(review_user=review_user,watchlist=watchlist)
        if query.exists():
            raise ValidationError("You already reviewd this watchlist")
        
        if watchlist.total_rating ==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating*watchlist.total_rating+serializer.validated_data['rating'])/(watchlist.total_rating+1)    
        watchlist.total_rating=watchlist.total_rating+ 1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=review_user)



             


#concrete class based view
#this will display all the reviews specific to a movie
class WatchListSpecificReviewList(generics.ListAPIView):
    serializer_class=ReviewSerializer
    # permission_classes=[IsAuthenticated]
    
    #customized thottling for this view only
    # throttle_classes =[ReviewListThrottling]
    
    #to 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']
    
    def get_queryset(self):
        watchlist_id=self.kwargs.get('pk')
        return Review.objects.filter(watchlist=watchlist_id)
    
#concrete class based view
#this will display all reviews not specific to a movie
class ReviewListView(generics.ListCreateAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    # builtin permission class
    # permission_classes=[IsAuthenticated]
    
    #for controling the number of acesses for user and anonymous users
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    
    

#concrete class based view
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer 
    
    # builtin permission class
    # permission_classes=[IsAuthenticatedOrReadOnly]
    
    #custom permission
    # permission_classes=[AdminOrReadOnly]  
    
    permission_classes=[IsAuthorOrReadOnly,IsAuthenticated]  
    
    # permission_classes=[IsAuthenticated]

    # authentication_classes = [TokenAuthentication]
    
    #alternate method for creatting view specific throttling
    throttle_classes=[ScopedRateThrottle]
    throttle_scope="review-detail"






# class based views with the concept of mixins
# class ReviewListView(mixins.CreateModelMixin,mixins.ListModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
        

# class ReviewDetailView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)




    

# class based view by extending APIView
class StreamPlatformListAPIView(APIView):
    permission_classes=[AdminOrReadOnly]#only admin can edit
    def get(self, request):
        stream_platform=StreamPlatform.objects.all()
        # stream_platform_serializer = StreamPlatformSerializer(stream_platform,many=True ,context={'request':request}) in case of hyperlinked related field we need to pass the request to next view
        stream_platform_serializer = StreamPlatformSerializer(stream_platform,many=True ,)
        return Response(stream_platform_serializer.data)
    
    def post(self, request):
        stream_platform_serializer = StreamPlatformSerializer(data=request.data)
        if stream_platform_serializer.is_valid():
            stream_platform_serializer.save()
            return Response(stream_platform_serializer.data,status=status.HTTP_201_CREATED)
        else:
             return Response(stream_platform_serializer.errors) 


class StreamPlatformDetailsAPIView(APIView):
    permission_classes=[AdminOrReadOnly]#only admin can edit
    
    def get(self, request,pk):
        stream_platform=StreamPlatform.objects.get(pk=pk)
        # stream_platform_serializer = StreamPlatformSerializer(stream_platform,context={'request':request}  )#in case of hyperlinked related field we need to pass the request to next view
        stream_platform_serializer = StreamPlatformSerializer(stream_platform,)
        return Response(data=stream_platform_serializer.data, status=status.HTTP_200_OK )
    
    def put(self, request,pk):
        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        stream_platform_serializer=StreamPlatformSerializer(stream_platform,request.data)
        if stream_platform_serializer.is_valid():
            stream_platform_serializer.save()
            return Response(stream_platform_serializer.data)
        else:
             return Response(stream_platform_serializer.errors) 
         
    def delete(self, request,pk):    
        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        stream_platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


#new class for listing watchlists to implement search condition
class WatchListSearchView(generics.ListAPIView):
    queryset=WatchList.objects.all()
    serializer_class=WatchListSerializer
    
    #search condition
    filter_backends = [filters.SearchFilter]
    search_fields  = ['title','platform__name']
   
#new class for listing watchlists to implement ordering condition    
class WatchListOrderingView(generics.ListAPIView):
    queryset=WatchList.objects.all()
    serializer_class=WatchListSerializer
    
    #in case of pagenumber pagination
    # pagination_class=WatchListPagination
    
    #in case of limitoffset pagination
    # pagination_class=WatchListLimitOffsetPagination
    
     #in case of cursor pagination
    pagination_class=WatchListCursorPagination
    
    
    #ordering condition
    #should comment when cursor pagination is used because it takes default ordering with created
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields   = ['avg_rating',] 
       
    



class WatchListAPIView(APIView):
    permission_classes=[AdminOrReadOnly]#only admin can post
    
    def get(self, request,):
        movie=WatchList.objects.all()
        movie_serializer = WatchListSerializer(movie,many=True, )
        return Response(movie_serializer.data)
    
    def post(self, request,):
        movie_serializer = WatchListSerializer(data=request.data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return Response(movie_serializer.data,status=status.HTTP_201_CREATED)
        else:
             return Response(movie_serializer.errors) 


class WatchListDetailsAPIView(APIView):
    permission_classes=[AdminOrReadOnly]#only admin can edit
    
    def get(self, request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie_serializer = WatchListSerializer(movie,)
        return Response(data=movie_serializer.data, status=status.HTTP_200_OK , )
    
    def put(self, request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        movie_serializer=WatchListSerializer(movie,request.data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return Response(movie_serializer.data)
        else:
             return Response(movie_serializer.errors) 
         
    def delete(self, request,pk):    
        try:
            movie = WatchList.objects.get(pk=pk)
        except:
            return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





#class based view for listing all movies and submitting new movie for initial lectures
#this class only accepts get and post
# class WatchListAPIView(APIView):
    
#     def get(self, request,):
#         movie=Movie.objects.all()
#         movie_serializer = MovieSerializer(movie,many=True)
#         return Response(movie_serializer.data)
    
#     def post(self, request,):
#         movie_serializer = MovieSerializer(data=request.data)
#         if movie_serializer.is_valid():
#             movie_serializer.save()
#             return Response(movie_serializer.data,status=status.HTTP_201_CREATED)
#         else:
#              return Response(movie_serializer.errors) 


# class WatchListDetailsAPIView(APIView):
    
#     def get(self, request,pk):
#         movie=Movie.objects.get(pk=pk)
#         movie_serializer = MovieSerializer(movie)
#         return Response(data=movie_serializer.data, status=status.HTTP_200_OK )
    
#     def put(self, request,pk):
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except:
#             return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
#         movie_serializer=MovieSerializer(movie,request.data)
#         if movie_serializer.is_valid():
#             movie_serializer.save()
#             return Response(movie_serializer.data)
#         else:
#              return Response(movie_serializer.errors) 
         
#     def delete(self, request,pk):    
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except:
#             return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT) 
                

        


#**********************************************************************************************
#function based views
#decorator is must
# @api_view(['GET'])
# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method == 'GET':
#          movies = Movie.objects.all()
#          movie_serializer=MovieSerializer(movies,many=True)
#          return Response(movie_serializer.data)
   
#     if request.method == 'POST':
#          movie_serializer=MovieSerializer(data=request.data)
#          if movie_serializer.is_valid():
#              movie_serializer.save()
#              return Response(movie_serializer.data,status=201)
#          else:
#              return Response(movie_serializer.errors)
       
       
          
   
   
# @api_view(['GET','PUT','DELETE'])    
# def movie_detail(request,pk):
#     if request.method =="GET":
        
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except:
#             return Response(data={"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)
                
            
#         movie_serializer=MovieSerializer(movie)
#         return Response(movie_serializer.data)
#     if request.method =="PUT":
#         movie = Movie.objects.get(pk=pk)
#         movie_serializer=MovieSerializer(movie,data=request.data)#we nee to pass old instance and new instance for updation
#         if movie_serializer.is_valid():
#              movie_serializer.save()
#              return Response(movie_serializer.data)
#         else:
#              return Response(movie_serializer.errors) 
        
#     if request.method =="DELETE":
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(data={"status": "success"}, status=status.HTTP_204_NO_CONTENT)
    
#*****************************************************************************************

        
        
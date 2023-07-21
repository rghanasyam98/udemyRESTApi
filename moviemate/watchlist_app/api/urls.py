from watchlist_app.api import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter
 
router=DefaultRouter()
router.register('streamplatform',views.StreamPlatformViewSet,basename='streamplatform')
 
urlpatterns = [
    path("watch_list/", views.WatchListAPIView.as_view(), name="movie-list"),
    #for applying search condition
    path("watch_list_search/", views.WatchListSearchView.as_view(), name="movie-list-search"),
    #for applying ordering condition
    path("watch_list_order/", views.WatchListOrderingView.as_view(), name="movie-list-order"),
    
    path("watch_list_detail/<int:pk>/", views.WatchListDetailsAPIView.as_view(), name="movie-detail"),
    path("stream_platform_list/", views.StreamPlatformListAPIView.as_view(), name="stream-platform-list"),
    path("stream_platform_list_detail/<int:pk>/", views.StreamPlatformDetailsAPIView.as_view(), name="stream-platform-list-detail"),
    path("review_list/", views.ReviewListView.as_view(), name="review-list"),#THIS will display all the reviews not specific to any movie
    path("review_detail/<int:pk>/", views.ReviewDetailView.as_view(), name="review-detail"),
    path("watch_list/<int:pk>/review_list/", views.WatchListSpecificReviewList.as_view(), name="watch_list-review-list"),
    path("watch_list/<int:pk>/review_create/", views.WatchListSpecificReviewCreate.as_view(), name="watch_list-review-create"),
    path("",include(router.urls)),
    
    #in case of filter condition is passed in url
    # path("user_review_detail/<str:username>/", views.UserReview.as_view(), name="user-review-detail"),
    #in case of fliter condition is passed in params
    path("user_review_detail/", views.UserReview.as_view(), name="user-review-detail"),
]
 
 
#urls in case of class based views  for initial lectures
# urlpatterns = [
#     path("movie_list/", views.MovieListAPIView.as_view(), name="movie-list"),
#     path("movie_detail/<int:pk>/", views.MovieDetailsAPIView.as_view(), name="movie-detail"),
# ]
 
#urls in case of function based views 
# urlpatterns = [
#     path("movie_list/", views.movie_list, name="movie-list"),
#     path("movie_detail/<int:pk>/", views.movie_detail, name="movie-detail"),
# ]


# urlpatterns = [
#     path("movie_list",views.movie_list,name="movie-list"),
#     path("<int:pk>",views.movie_detail,name="movie-detail"),
# ]

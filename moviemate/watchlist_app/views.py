# from django.http import JsonResponse
# from django.shortcuts import render
# from . models import Movie
# # Create your views here.

# def movie_list(request):
#     movies=Movie.objects.all()
#     context={
#         'movies':list(movies.values())
#     }
#     return JsonResponse(context)


# def movie_detail(request,pk):
#     movie=Movie.objects.get(pk=pk)
#     context={
#         'name':movie.name,
#         'description':movie.description,
#         'active':movie.active
#     }
#     return JsonResponse(context)
    
    
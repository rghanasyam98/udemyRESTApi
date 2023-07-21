from rest_framework import serializers

# from watchlist_app.models import Movie
from watchlist_app.models import StreamPlatform, WatchList,Review




class ReviewSerializerForSpecificCreate(serializers.ModelSerializer):
    
    class Meta:
        model=Review
        # fields="__all__"
        # fields=['id','name','description','active']
        exclude =['watchlist','review_user']

class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)#the name of field in model
    watchlist=serializers.StringRelatedField(read_only=True)#the name of field in model
    class Meta:
        model=Review
        fields="__all__"
        # fields=['id','name','description','active']
        # exclude =['active']
        
    

class WatchListSerializer(serializers.ModelSerializer):
    # reviews=ReviewSerializer(read_only=True,many=True)#the related_name attribute in model
    name_length=serializers.SerializerMethodField()#this is a custom field
    
    #to display the platform of this watchlist (foreignkey connection)
    platform=serializers.CharField(source='platform.name')
    
    class Meta:
        model=WatchList
        fields="__all__"
        # fields=['id','name','description','active']
        # exclude =['active']
        
        
    #calculating value for custom field
    def get_name_length(self,obj):
        return len(obj.title)   
        
    
    

class StreamPlatformSerializer(serializers.ModelSerializer):
    #nested serializer=>for accessing foreign key related fields to get the list of watch list under that platform
    # this will display all fields
    watchlist=WatchListSerializer(many=True, read_only=True)#the related_name attribute in model
    # review_user=serializers.StringRelatedField(many=True, read_only=True)
    
    #to display only related models string field only
    # watchlist=serializers.StringRelatedField(many=True, read_only=True)
    
    #to display only related models pk field only
    # watchlist=serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    
    #this will display only hyperlinked field of related model
    #need to pass the request in context{'request':request} from this view to where we want to go
    # watchlist=serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     #this is the name of the view or url that we want to go
    #     view_name="movie-detail" 
    #     )

    class Meta:
        model=StreamPlatform
        fields="__all__"
        


        
   
        



#model serializer for movie model for initial lecture
# class MovieSerializer(serializers.ModelSerializer):
#     name_length=serializers.SerializerMethodField()#this is a custom field
#     class Meta:
#         model=Movie
#         fields="__all__"
#         # fields=['id','name','description','active']
#         # exclude =['active']
        
        
#     #calculating value for custom field
#     def get_name_length(self,obj):
#         return len(obj.name)   
        
#     #methods for validation
    
#     #field level validation => individual field is validated
#     def validate_name(self,name):
#         if len(name)<3:
#             raise serializers.ValidationError("Name must be at least 3 characters long")
#         return name
    
#     #object level validation => multiple fields is validated
#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description must be different")
#         return data


# #validator method for validating description
# def description_len_check(description):
#     if len(description)<5:
#         raise serializers.ValidationError("Description must be at least 3 characters long")
#     return description

# class MovieSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField()
#     description=serializers.CharField(validators=[description_len_check])#validator, the specified method should be defined separately
#     active=serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
    
#     #methods for validation
    
#     #field level validation => individual field is validated
#     def validate_name(self,name):
#         if len(name)<3:
#             raise serializers.ValidationError("Name must be at least 3 characters long")
#         return name
    
#     #object level validation => multiple fields is validated
#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description must be different")
#         return data
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class WatchListPagination(PageNumberPagination):
    #default pagination size
    page_size=1
    page_query_param='sheet'
    #pagination size for user selection
    #user can specify the number
    page_size_query_param='page_size'
    
    #maximum number of records can have in a page
    max_page_size=3
    
    #use sheet=last page to goto last page
    # last_page_strings='last_page'
    #also have another parameters
    
    
class WatchListLimitOffsetPagination(LimitOffsetPagination):
    default_limit=2
    max_limit =3
    limit_query_param ='limit'#customized name of limit in url
    offset_query_param = 'start'#customized name of offset in url
      
      
class WatchListCursorPagination(CursorPagination):
    page_size=2 
    ordering='created'    #reverse of default 
    # cursor_query_param='cursor1'
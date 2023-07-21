from rest_framework.throttling import UserRateThrottle,AnonRateThrottle


class ReviewCreateThrottling(UserRateThrottle):
    scope="review-create"
    
class ReviewListThrottling(UserRateThrottle):
    scope="review-list"    
from django.urls import path, include

from . import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/user-profile/', views.GetUserProfile.as_view()),
    # path('api/invvite-code/', views.EnterInviteCode.as_view()),
    ]
from django.urls import path
from .views import ReactionAPIView

urlpatterns = [
    path("<slug:slug>/", ReactionAPIView.as_view(), name="user-reaction"),
]

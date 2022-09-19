import stat
from authors_api.settings.local import DEFAULT_FROM_EMAIL
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import CantFollowYourself, NotYourProfile
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer

User = get_user_model()
# @api_view(["GET"])
# @permission_classes([permissions.AllowAny])
# def get_all_profiles(requests):
#     profiles = Profile.objects.all()
#     serializer = ProfileSerializer(profiles, many=True)
#     namespaced_response = {"profiles": serializer.data}
#     return Response(namespaced_response, status=status.HTTP_200_OK)


# @api_view(["GET"])
# @permission_classes([permissions.IsAuthenticated])
# def get_profile_details(request, username):
#     try:
#         specific_profile = Profile.objects.get(user__username=username)
#     except Profile.DoesNotExist:
#         raise NotFound("A profile with that username does not exist")
#     serializer = ProfileSerializer(specific_profile, many=False)
#     formatted_response = {"profile": serializer.data}
#     return Response(formatted_response, status=status.HTTP_200_OK)


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (ProfilesJSONRenderer,)
    pagination_class = ProfilePagination


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with that username doesn't exist")

        serializer = self.serializer_class(profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    renderer_classes = [ProfilesJSONRenderer]
    serialuizer_class = (UpdateProfileSerializer,)

    def patch(self, request, username):
        try:
            self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with that username doesn't exist")

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_my_followers(request, username):
    try:
        specific_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise NotFound("A user with that username doesn't exist...")
    userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
    user_followers = userprofile_instance.followed_by.all()
    serializer = FollowingSerializer(user_followers, many=True)
    formatted_response = {
        "status_code": status.HTTP_200_OK,
        "followers": serializer.data,
        "num_of_followers": len(serializer.data),
    }

    return Response(formatted_response, status=status.HTTP_200_OK)


class FollowUnfollowAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowingSerializer

    # Get All users I follow
    def get(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist ")

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        my_following_list = userprofile_instance.following_list.all()
        serializer = ProfileSerializer(my_following_list, many=True)
        formatted_response = {
            "users_i_follow": serializer.data,
            "status_code": status.HTTP_200_OK,
            "num_users_i_follow": len(serializer.data),
        }

        return Response(formatted_response, status=status.HTTP_200_OK)

    # Follow a specific user
    def post(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        if specific_user.pkid == request.user.pkid:
            raise CantFollowYourself

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        if current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You already follow {specific_user.username}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.follow(userprofile_instance)

        subject = "A new user follows you"
        message = f"Hi {specific_user.username}, the user {current_user_profile.user.username} now follows you"
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [specific_user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        return Response(
            {
                "status_code": status.HTTP_200_OK,
                "detail": f"You now follow {specific_user.username}",
            }
        )

    # Unfollow a specific user
    def delete(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        if not current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You do not follow {specific_user.username}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.unfollow(userprofile_instance)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "detail": f"You have unfollowed {specific_user.username}",
        }
        return Response(formatted_response, status=status.HTTP_200_OK)

from rest_framework.exceptions import APIException


class AlreadyFavourited(APIException):
    status_code = 400
    default_detail = "You have already favourited this article"

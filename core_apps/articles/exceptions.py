from rest_framework.exceptions import APIException


class UpdateArticleException(APIException):
    status_code = 403
    default_detail = "You can not update an article that does not belong to you"

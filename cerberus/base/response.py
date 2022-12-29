from django import http
from rest_framework.response import Response as DRFResonse


class Response(DRFResonse):
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        super().__init__(data, status, template_name, headers, exception, content_type)




class Created(Response):
    
    status_code = 201
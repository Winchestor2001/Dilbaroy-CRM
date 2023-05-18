from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import APIView


class HomeAPI(APIView):
    def get(self, request):
        context = [
            {
                'company': "Dilbaroy Clinik"
            }
        ]
        return Response({'status': '(403) Permission denied', 'context': context}, status=403)

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class CallbackPayment(ListAPIView):

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)





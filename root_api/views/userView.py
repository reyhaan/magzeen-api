from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..utils.serializers import UserSerializer

class UserView(viewsets.ViewSet):
    """ this is an example of viewset """

    serializer = UserSerializer

    def list(self, request):
        return Response({'message': 'this is some data from VIEWSET'})

    def create(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response({'message': 'retrieve method'})

    def update(self, request, pk=None):
        return Response({'message': 'UPDATE method'})

    def partial_update(self, request, pk=None):
        return Response({'message': 'PARTIAL_UPDATE method'})
    
    def destroy(self, request, pk=None):
        return Response({'message': 'DESTROY method'})
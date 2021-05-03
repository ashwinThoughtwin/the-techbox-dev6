from .models import TechItem, AllottedItem, Employee
from .serializer import TechItemSerializer, AssignItemSerializer, EmployeeSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TechitemList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        techitem = TechItem.objects.all()
        serializer = TechItemSerializer(techitem, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TechItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TechItemDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return TechItem.objects.get(pk=pk)
        except TechItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        techitem = self.get_object(pk)
        serializer = TechItemSerializer(techitem)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        techitem = self.get_object(pk)
        serializer = TechItemSerializer(techitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        techitem = self.get_object(pk)
        techitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignItemApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        assignitem = AllottedItem.objects.all()
        serializer = AssignItemSerializer(assignitem, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AssignItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeCreate(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)

# class AssignItemApi(generics.ListCreateAPIView):
#     queryset = AllottedItem.objects.all()
#     serializer_class = AssignItemSerializer
#     # permission_classes = (IsAuthenticated,)


# class EmployeeCreate(generics.CreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     # permission_classes = (IsAuthenticated,)
#
#
# class TechItemUpdate(generics.UpdateAPIView):
#     queryset = TechItem.objects.all()
#     serializer_class = TechItemSerializer
#     permission_classes = (IsAuthenticated,)
#
#
# class TechItemList(generics.ListAPIView):
#     queryset = TechItem.objects.all()
#     serializer_class = TechItemSerializer
#     permission_classes = (IsAuthenticated,)
#
#
# class TechItemDelete(generics.DestroyAPIView):
#     queryset = TechItem.objects.all()
#     serializer_class = TechItemSerializer
#     permission_classes = (IsAuthenticated,)

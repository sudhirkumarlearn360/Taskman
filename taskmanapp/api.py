from rest_framework import serializers
from rest_framework.decorators import APIView
from django.http import Http404
from rest_framework.response import Response
from .models import Task
from rest_framework import status

class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =  '__all__'

class TaskListAPI(APIView):
    '''
    API View for task created
    '''
    def get(self,request):
        task_obj = Task.objects.all()
        serializer = TaskSerializers(task_obj,many=True)
        return Response({'status':200,'payload':serializer.data})
    
    def post(self,request):
        task_obj = TaskSerializers(data = request.data)
        if task_obj.is_valid():
            task_obj.save()
            return Response(task_obj.data, status=status.HTTP_201_CREATED)
        return Response(task_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TaskDetailAPI(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, id):
        try:
            return Task.objects.get(pk=id)
        except Task.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        task_delete = self.get_object(id)
        task_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, id, format=None):
        task_obj = self.get_object(id)
        serializer = TaskSerializers(task_obj,many=False)
        return Response({'status':200,'payload':serializer.data})
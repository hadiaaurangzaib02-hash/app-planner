from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Task 
import logging 
logger = logging.getLogger('django')

# Create a new task from form
class CreateTaskView(APIView) :
    def post(self, request) :
        try :
            name = request.data['name']
            video_url = request.data['video_url'] if 'video_url' in request.data else None
            description = request.data['description'] if 'description' in request.data else None
            audio = request.FILES['audio'] if 'audio' in request.FILES else None
        
            if description =='null' :
                description = None 
            if video_url == 'null' :
                video_url = None 
            if audio == 'null' :
                audio = None 
            
            if name is False:
                return Response(status = status.HTTP_401_UNAUTHORIZED)

            Task.objects.create(name = name,
                                video_url = video_url,
                                description = description,
                                user = request._user,
                                audio = audio)
                
        except Exception as e :
            logger.error("[CREATE TASK] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status = status.HTTP_201_CREATED)

# Edit a current task 
class EditTaskView(APIView) :
    def post(self, request) :
        try :
            task_id = request.data['task_id']
            name = request.data['name'] if 'name' in request.data else None
            video_url = request.data['video_url'] if 'video_url' in request.data else None
            description = request.data['description'] if 'description' in request.data else None
            display = request.data['display'] if 'display' in request.data else None
            audio = request.FILES['audio'] if 'audio' in request.FILES else None

            if description =='null' :
                description = None 
            if video_url == 'null' :
                video_url = None 
            if audio == 'null' :
                audio = None 
            if display == 'null' :
                display = None
            if task_id is False:
                return Response(status = status.HTTP_401_UNAUTHORIZED)
            
            current_task = Task.objects.get(pk = task_id, user = request._user)
            if name :
                current_task.name = name 
            if video_url : 
                current_task.video_url = video_url 
            if description :
                current_task.description = description 
            if display :
                current_task.display = display
            if audio : 
                current_task.audio = audio
            current_task.save()
                
        except Exception as e :
            logger.error("[SAVE TASK] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status = status.HTTP_200_OK)

# Get a current task 
class GetTaskByIdView(APIView) :
    def post(self, request) :
        try :
            task_id = request.data['task_id']
            if task_id is False:
                return Response(status = status.HTTP_401_UNAUTHORIZED)
            
            current_task = Task.objects.get(pk = task_id, user = request._user)
             
        except Exception as e :
            logger.error("[GET TASK BY ID] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            response_json = {'name' : current_task.name,
                        'description' : current_task.description,
                        'video_url' : current_task.video_url}
            if current_task.audio :
                response_json['audio'] = str(current_task.audio)
            return Response(response_json, 
                        status = status.HTTP_200_OK)

# Get all current tasks
class SearchTaskView(APIView) :
    def get(self, request) :
        try :
            tasks = Task.objects.filter(user = request._user).order_by('-created_datetime')
        
            if len(tasks) > 0 :
                task_result_list = []
                for task in tasks :
                    task_dict = {
                        'id' : task.pk,
                        'name' : task.name,
                        'show_hidden' : task.display
                    }
                    task_result_list.append(task_dict)
                return Response({'tasks' : task_result_list}, status = status.HTTP_200_OK)
            else :
                return Response(status = status.HTTP_204_NO_CONTENT)
        except Exception as e :
            logger.error("[SEARCH TASKS] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete task by ID
class DeleteTaskView(APIView) :
    def get(self, request, task_id) :
        try :
            if task_id is False:
                return Response(status = status.HTTP_401_UNAUTHORIZED)
         
            Task.objects.get(pk = task_id, user = request._user).delete()

        except Exception as e :
            logger.error("[DELETE TASK] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status = status.HTTP_200_OK)

# Change display
class DisplayTaskChangeView(APIView) :
    def post(self, request) :
        try :
            task_id = request.data['task_id']
            if task_id is False:
                return Response(status = status.HTTP_401_UNAUTHORIZED)
         
            task_object = Task.objects.get(pk = task_id, user = request._user)
            if task_object.display :
                task_object.display = False
            else :
                task_object.display = True
            task_object.save()
            return Response(status = status.HTTP_200_OK)
        except Exception as e :
            logger.error("[CHANGE DISPLAY] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
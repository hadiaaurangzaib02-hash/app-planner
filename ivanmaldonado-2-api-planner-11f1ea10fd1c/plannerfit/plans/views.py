from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Plan 
import logging 
logger = logging.getLogger('django')
import json


from users.models import Client

# Create your views here.

'''
    steps = [
        {
            task : ...,
            series : ....,
            ...
        }
    ]
'''

class CreatePlanView(APIView) :
    def post(self, request) :
        try :
            name = request.data['name']
            observations = request.data['observations'] if 'observations' in request.data else None
            steps = request.data['steps'] if 'steps' in request.data else None

            if name is False:
                return Response(status = status.HTTP_401_UNAUTHORIZED)
            
            if steps :
                steps_count = len(steps['data']['tasks'])
                steps = json.dumps(steps)
            new_plan = Plan.objects.create(name = name, observations = observations,
                                        steps = steps, 
                                        steps_count = steps_count,
                                        trainer = request._user)
            new_plan.save()        
        except Exception as e :
            logger.error("[CREATE PLAN] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response({'plan': new_plan.pk}, status = status.HTTP_201_CREATED)

# Get all current tasks
class ListAllPlansView(APIView) :
    def get(self, request) :
        try :
            plans = Plan.objects.filter(trainer = request._user).order_by('-created_datetime')
            if len(plans) > 0 :
                plan_result_list = []
                for plan in plans :
                    plan_dict = {
                        'id' : plan.pk,
                        'name' : plan.name,
                        'count_tasks' : plan.steps_count
                    }
                    plan_result_list.append(plan_dict)
                return Response({'plans' : plan_result_list}, status = status.HTTP_200_OK)
            else :
                return Response(status = status.HTTP_204_NO_CONTENT)
        except Exception as e :
            logger.error("[ALL TASK VIEW] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeletePlanView(APIView) :
    def get(self, request, plan_id) :
        try :
            plan = Plan.objects.get(pk = plan_id, trainer = request._user)
            plan.delete()
        except Exception as e :
            logger.error("[DELETE PLAN] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status = status.HTTP_200_OK)

class ShowPlanView(APIView) :
    def get(self, request, plan_id) :
        try :
            plan = Plan.objects.get(pk = plan_id, trainer = request._user)
            
            plan_info = {
                'name' : plan.name,
                'observations' : plan.observations,
            }
            if plan.steps :
                plan_info['steps'] = json.loads(plan.steps)
            
            
        except Exception as e :
            logger.error("[SHOW PLAN INFO] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(plan_info, status = status.HTTP_200_OK)

class EditPlaniew(APIView) :
    def post(self, request) :
        try :
            name = request.data['name'] 
            plan_id = request.data['plan_id'] 
            observations = request.data['observations'] if 'observations' in request.data else None
            steps = request.data['steps'] if 'steps' in request.data else None
          
            if plan_id is False:
                return Response(status = status.HTTP_401_UNAUTHORIZED)

            plan = Plan.objects.get(pk = plan_id, trainer = request._user)
            plan.name = name 
            plan.observations = observations
            plan.steps = json.dumps(steps)
           
            plan.save()        
        except Exception as e :
            logger.error("[EDIT PLAN] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status = status.HTTP_200_OK)

class AddClientToPlan(APIView) :
    def post(self, request) :
        try :
            client_id = int(request.data['client_id'])
            plan_id = int(request.data['plan_id'])   
            client_object = Client.objects.get(pk = client_id, trainer = request._user)
            plan_object = Plan.objects.get(pk = plan_id, trainer = request._user)
            client_object.plans_assigned.add(plan_object)
            client_object.save()        
        except Exception as e :
            logger.error("[ADD CLIENT TO PLAN] "+str(e))
            return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status = status.HTTP_200_OK)
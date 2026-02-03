from django.shortcuts import render
from users.mail import send_mail
from users.models import Trainer, Client
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from plans.models import Plan 

import logging 
logger = logging.getLogger('django')
# Create your views here.
class UserRegister(APIView) :
    permission_classes = (permissions.AllowAny,)
    def post(self, request) :
        try :
            email = request.data['email']
            
            if email is False:
                return Response(status.HTTP_401_UNAUTHORIZED)
            
            new_user = Trainer.objects.create(email = email)
                     
            token = Token.objects.get_or_create(user=new_user)[0].key
            
            if token :
                code = new_user.generate_random_code()
                ## ENVIAR EMAIL
                message = 'Este es tu código de acceso: '+str(code)
                subject = 'Código acceso plannerfit'
                send_mail(message, subject, email)

                return Response({'accessToken' : token, 'user' : email}, status.HTTP_201_CREATED)
        except Exception as e :
            logger.error("[USER REGISTER] "+str(e))
            return Response({'error' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class UserLogin(APIView) :
    permission_classes = (permissions.AllowAny,)
    def post(self, request) :
        try :
            code = request.data['code'] if 'code' in request.data else False
            if code is False:
                return Response(status.HTTP_401_UNAUTHORIZED)
            
            try :
                user = Trainer.objects.get(code = code)
            except Trainer.DoesNotExist :
                return Response(status.HTTP_401_UNAUTHORIZED)
            else :
                if user.check_code(code) :
                    token = Token.objects.get_or_create(user=user)[0].key
                    user.clear_code()

                    return Response({'accessToken' : token, 'user' : user.email}, status.HTTP_201_CREATED)
                
        except Exception as e :
            logger.error("[USER REGISTER] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class UserCode(APIView) :
    permission_classes = (permissions.AllowAny,)
    def post(self, request) :
        try :
            email = request.data['email']
            if email is False:
                return Response(status.HTTP_401_UNAUTHORIZED)
            
            try :
                new_user = Trainer.objects.get(email = email)
            except Trainer.DoesNotExist :
                return Response(status.HTTP_401_UNAUTHORIZED)
            else :
                if not new_user.check_integrity_code() :
                    code = new_user.generate_random_code()
                    ## ENVIAR EMAIL
                    message = 'Este es tu código de acceso: '+str(code)
                    subject = 'Código acceso plannerfit'
                    send_mail(message, subject, email)
                return Response(status=status.HTTP_200_OK)
                
        except Exception as e :
            logger.error("[USER CODE] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserEdit(APIView) :
    def post(self, request) :
        try :
            nickname = request.data['nickname'] if 'nickname' in request.data else None 
            username = request.data['name'] if 'name' in request.data else None 
            surname = request.data['surname'] if 'surname' in request.data else None    
            user = Trainer.objects.get(email = request._user)            
            if nickname :
                user.nickname = nickname 
            if username :
                user.username = username 
            if surname :
                user.surname = surname 
            user.save()    
        except Exception as e :
            logger.error("[USER EDIT] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status=status.HTTP_200_OK)


####### CLIENTS
class AddClient(APIView) :
    def post(self, request) :
        try :
            name = request.data['name'] if 'name' in request.data else None 
            surname = request.data['surname'] if 'surname' in request.data else None 

            if not name or not surname :
                return Response(status.HTTP_401_UNAUTHORIZED)

            phone = request.data['phone'] if 'phone' in request.data else None    
            email = request.data['email'] if 'email' in request.data else None 
            observations = request.data['observations'] if 'observations' in request.data else None   
            new_client = Client.objects.create(name = name, trainer = request._user)         
            if surname :
                new_client.surname = surname 
            if phone :
                new_client.phone = phone 
            if email :
                new_client.email = email 
            if observations :
                new_client.observations = observations 
            new_client.save()    
        except Exception as e :
            logger.error("[ADD CLIENT] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status=status.HTTP_201_CREATED)

class DeleteClient(APIView) :
    def get(self, request, client_id) :
        try :      
            client = Client.objects.get(pk = client_id, trainer = request._user)         
            client.delete()
        except Exception as e :
            logger.error("[DELETE CLIENT] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status=status.HTTP_200_OK)

class ListClients(APIView) :
    def get(self, request) :
        try :  
            clients = Client.objects.filter(trainer = request._user)         
            
            if len(clients) > 0 :
                returned_client_list = []
                for client in clients :
                    client_dict = {}
                    client_dict['id'] = client.pk 
                    client_dict['name'] = client.name 
                    client_dict['surname'] = client.surname
                    client_dict['status'] = client.status
                    plans_assigned = 0
                    plans_completed = 0
                    if client.plans_assigned.exists():
                        plans_assigned = client.plans_assigned.count() 
                    if client.plans_completed.exists() :
                        plans_completed = client.plans_completed.count() 
                    plans_pending = plans_assigned - plans_completed
                    client_dict['pending_plans'] = plans_pending
                    if client.last_plan :
                        client_dict['pending_plans'] = client.last_plan.name
                    else :
                        client_dict['pending_plans'] = ''
                    returned_client_list.append(client_dict)
                
                return Response({'clients' : returned_client_list}, status=status.HTTP_200_OK) 
            else :
                return Response(status=status.HTTP_204_NO_CONTENT) 
        except Exception as e :
            logger.error("[LIST CLIENT] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientChangeStatus(APIView) :
    def post(self, request) :
        try :     
            client_id = request.data['client_id']
            client = Client.objects.get(pk = client_id, trainer = request._user)         
            
            if client.status :
                client.status = False 
            else :
                client.status = True
            client.save()    
        except Exception as e :
            logger.error("[CHANGE CLIENT STATUS] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status=status.HTTP_200_OK)

class ClientGetData(APIView) :
    def get(self, request, client_id) :
        try :     
            client = Client.objects.get(pk = client_id, trainer = request._user)  
            client_dict = {
                'name' : client.name.capitalize(),
                'surname': client.surname.capitalize(),
                'email' : client.email,
                'phone' : client.phone,
                'observations' : client.observations,
                'plans_assigned' : [],
                'plans_assigned_cnt' : 0,
                'plans_completed_cnt' : 0, 
                'plans_discarded_cnt' : 0,
                'plans_favorite_cnt' : 0,
                'last_login' : ''
            }     
            if client.plans_assigned.exists() :
                plans = []
                for plan in client.plans_assigned.all() :
                    plan_dict = {
                        'id' : plan.pk,
                        'name' : plan.name
                    }
                    plans.append(plan_dict)
                client_dict['plans_assigned'] = plans 
                client_dict['plans_assigned_cnt'] = client.plans_assigned.count()
            if client.plans_completed.exists() :
                client_dict['plans_completed_cnt'] = client.plans_completed.count()
            if client.plans_completed.exists() :
                client_dict['plans_discarded_cnt'] = client.plans_discarded.count()
            if client.plans_favorite.exists() :
                client_dict['plans_favorite_cnt'] = client.plans_favorite.count()
            if client.last_login_datetime :
                client_dict['last_login'] = client.last_login_datetime.strftime("%m/%d/%Y, %H:%M:%S")
        
        except Exception as e :
            logger.error("[CHANGE CLIENT STATUS] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(client_dict, status=status.HTTP_200_OK)

class AddPlaToClientView(APIView) :
    permission_classes = (permissions.AllowAny,)
    def post(self, request) :
        try :
            plan_id = request.data['plan_id']
            client_id = request.data['client_id']
            if plan_id is False or client_id is False:
                return Response(status.HTTP_401_UNAUTHORIZED)
            if plan_id :
                plan_id = int(plan_id)
            if client_id :
                client_id = int(client_id)
            client = Client.objects.get(pk=client_id)
            plan = Plan.objects.get(pk=plan_id)

            client.plans_assigned.add(plan)
            client.save()   
        except Exception as e :
            logger.error("[ADD PLAN TO CLIENT] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status=status.HTTP_200_OK)

class RemovePlanFromClient(APIView) :
    def get(self, request, client_id, plan_id) :
        try :     
            if plan_id is False or client_id is False:
                return Response(status.HTTP_401_UNAUTHORIZED)
            client = Client.objects.get(pk=client_id)
            plan = Plan.objects.get(pk=plan_id)

            client.plans_assigned.remove(plan)  
            client.save()
        except Exception as e :
            logger.error("[REMOVE PLAN FROM CLIENT] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status=status.HTTP_200_OK)

class GetOrCreateClientLink(APIView) :
    def get(self, request, client_id) :
        try :     
            if client_id is False or client_id is False:
                return Response(status.HTTP_401_UNAUTHORIZED)
            client = Client.objects.get(pk=client_id)

            if not client.link :
                client.link = client.name.replace(" ", "-").lower() + "-" +client.surname.replace(" ", "-").lower()
                client.save()
        except Exception as e :
            logger.error("[CREATE-CLIENT-LINK] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response({'link' : 'https://plannerfit.edufitness.online/pt/'+client.link}, status=status.HTTP_200_OK)

class SendClientLinkByEmail(APIView) :
    def get(self, request, client_id) :
        try :     
            if client_id is False or client_id is False:
                return Response(status.HTTP_401_UNAUTHORIZED)
            client = Client.objects.get(pk=client_id)
            if request._user.username :
                trainer_name = request._user.username
            else :
                trainer_name = request._user.email
            if client.email :
                link = 'https://plannerfit.edufitness.online/pt/'+client.link
                 ## ENVIAR EMAIL
                message = '''<h3>Bienvenido a Plannerfit!</h3><p>El entrenador '''+trainer_name.capitalize()+''' 
                           te envía el siguiente enlace de acceso a la plataforma: <br /><a href="'''+link+'''" target="_blank">'''+link+'''</a>'''
                subject = 'Bienvenido a Plannerfit!'
                send_mail(message, subject, client.email)
            else :
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e :
            logger.error("[SEND USER LINK] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status=status.HTTP_200_OK)

class GetClientData(APIView) :
    def get(self, request, client_id) :
        try :     
            if client_id is False:
                return Response(status.HTTP_401_UNAUTHORIZED)
            client = Client.objects.get(pk=client_id)
            
            client_dict = {
                'name' : client.name,
                'surname' : client.surname,
                'email' : client.email,
                'phone' : client.phone,
                'observations' : client.observations
            }
        except Exception as e :
            logger.error("[GET CLIENT DATA] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(client_dict, status=status.HTTP_200_OK)

class EditClient(APIView) :
    def post(self, request) :
        try :
            name = request.data['name'] if 'name' in request.data else None 
            surname = request.data['surname'] if 'surname' in request.data else None 
            client_id = request.data['client_id'] if 'client_id' in request.data else None
            if not name or not surname :
                return Response(status.HTTP_401_UNAUTHORIZED)

            phone = request.data['phone'] if 'phone' in request.data else None    
            email = request.data['email'] if 'email' in request.data else None 
            observations = request.data['observations'] if 'observations' in request.data else None   
            client = Client.objects.get(pk = client_id, trainer = request._user)         
            if name :
                client.name = name 
            if surname :
                client.surname = surname 
            if phone :
                client.phone = phone 
            if email :
                client.email = email 
            if observations :
                client.observations = observations 
            client.save()    
        except Exception as e :
            logger.error("[EDIT CLIENT] "+str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else :
            return Response(status=status.HTTP_200_OK)
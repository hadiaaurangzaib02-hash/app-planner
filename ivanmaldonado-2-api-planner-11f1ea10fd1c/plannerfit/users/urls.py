from django.urls import path

from users.views import (UserCode, UserRegister, UserLogin, 
                UserEdit, ListClients, AddClient,ClientChangeStatus,
                ClientGetData,DeleteClient, AddPlaToClientView,
                RemovePlanFromClient,GetOrCreateClientLink, SendClientLinkByEmail,
                EditClient)

urlpatterns = [
    # Users
    path('login', UserLogin.as_view()),
    path('edit', UserEdit.as_view()),
    path('register', UserRegister.as_view()),
    path('code', UserCode.as_view()),
    path('clients/edit', EditClient.as_view()),
    path('clients/all', ListClients.as_view()),
    path('clients/new', AddClient.as_view()),
    path('clients/change/status', ClientChangeStatus.as_view()),
    path('clients/<int:client_id>', ClientGetData.as_view()),
    path('clients/delete/<int:client_id>', DeleteClient.as_view()),
    path('clients/add/plan', AddPlaToClientView.as_view()),
    path('clients/<int:client_id>/remove/plan/<int:plan_id>', RemovePlanFromClient.as_view()),
    path('clients/<int:client_id>/link', GetOrCreateClientLink.as_view()),
    path('clients/<int:client_id>/linkEmail', SendClientLinkByEmail.as_view()),
]
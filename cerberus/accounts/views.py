# from django.shortcuts import render
# from django_keycloak.backends import KeycloakAuthenticationBackend as user_auth
# from django.views.generic import View
# from django.http import HttpResponse
# from django.contrib.auth import get_user_model
# from django_keycloak.models import KeycloakUserAutoId
# from django.contrib.auth import login


# class LoginView(View):

#     def get(self, request):

#         user_model = get_user_model()

#         print(user_model)

#         for f in KeycloakUserAutoId._meta.get_fields():
#             print(f)

#         users = KeycloakUserAutoId.objects.all()
#         print(users)

#         return render(
#             request, 
#             "accounts/login.html", 
#             {},
#             )

#     def post(self,request):
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         print("Username :", username, "password :", password)

#         # user = user_auth.authenticate(request, username, password)
#         # if user.is_authenticated:
#         #     login(user)

#         user = KeycloakUserAutoId.objects.create(keycloak_id = 1, username= username, password=password)
#         user.save()

#         print(user)
     
#         # user = authenticate(username, password)
#         # if user.is_authenticated:
#         #     print("User Logged in")
#         #     login(user)
        
#         print("Condition passed")
#         return HttpResponse("Hello User %s",user)
        
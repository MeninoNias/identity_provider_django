from django.urls import path, include

urlpatterns = [
    path('api/', include('service.api.v1.urls')),
]

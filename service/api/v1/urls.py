from django.urls import path

from service.api.v1.views import SingInAPIView

urlpatterns = [
    path('singin', SingInAPIView.as_view(), name='sing-in'),
]

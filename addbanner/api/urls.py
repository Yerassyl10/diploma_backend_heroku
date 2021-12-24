from django.urls import path
from addbanner.api.views import AddsBannerListAPIView, add_banner_view
app_name = 'addbanner'

urlpatterns = [
    path('adds/', AddsBannerListAPIView.as_view(), name="adds"),
    path('adds/<int:add_id>', add_banner_view),
]
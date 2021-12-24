from django.contrib import admin
from django.urls import path, include


from api.views import detailed_opportunity_view, subscribed_opportunities_view, favourate_pressed_view, \
    favourate_opportunities_view, company_detail, opportunities_by_company, subscribe_pressed_view, \
    subscribed_companies_list, CompaniesAPIView, all_opportunities_view, all_job_categories_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.api.urls', 'account_api')),
    path('api/addbanner/', include('addbanner.api.urls', 'addbanner_api')),
    path('verify/', include('verification.urls')),
    path('api/opportunities/<int:id>/', detailed_opportunity_view),
    path('api/subscribed_opportunities/', subscribed_opportunities_view),
    path('api/favourate_pressed/<int:opportunity_id>/', favourate_pressed_view),
    path('api/favourate_opportunities/', favourate_opportunities_view),
    path('api/companies/<int:company_id>', company_detail),
    path('api/companies/<int:company_id>/opportunities', opportunities_by_company),
    path('api/subscribe_pressed/<int:company_id>/', subscribe_pressed_view),
    path('api/subscribed_companies/', subscribed_companies_list),
    path('api/companies/', CompaniesAPIView.as_view()),
    path('api/opportunities/', all_opportunities_view),
    path('api/job_categories/', all_job_categories_view),
]

from django_filters import rest_framework as filters

from api.models import Opportunity


class OpportunityFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Opportunity
        fields = ('title', 'job_type', 'company', 'deadline', 'job_category', 'location', 'contract_type')

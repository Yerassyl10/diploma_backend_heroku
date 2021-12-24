import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Company, Opportunity, Subscription, Favourate,  JobCategory
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.serializers import CompanySerializer, OpportunitySerializer
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import OpportunityFilter
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt



def detailed_opportunity_view(request, id):
    context = {'data': {}}
    opportunity = Opportunity.objects.get(id=id)
    context['data']['id'] = opportunity.id
    context['data']['title'] = opportunity.title
    context['data']['job_type'] = opportunity.job_type
    context['data']['description'] = opportunity.description
    context['data']['key_benefits'] = opportunity.key_benefits
    context['data']['deadline'] = opportunity.deadline
    context['data']['requirements'] = opportunity.requirements
    context['data']['read_more_link'] = opportunity.read_more_link
    context['data']['apply_link'] = opportunity.apply_link

    context['data']['company'] = {
        'name': opportunity.company.name,
        'about_company': opportunity.company.about_company,
        'picture': opportunity.company.picture.url,
    }

    if request.user.id:
        try:
            Favourate.objects.get(user=request.user, opportunity=opportunity)
            context['data']['is_favourate'] = True
        except Favourate.DoesNotExist:
            context['data']['is_favourate'] = False
    else:
        context['data']['is_favourate'] = False

    context['data']['location'] = opportunity.location
    context['data']['contract_type'] = opportunity.contract_type

    if opportunity.job_category:
        context['data']['job_category'] = {
            'id': opportunity.job_category.id,
            'title': opportunity.job_category.title,
        }
    else:
        context['data']['job_category'] = None

    return JsonResponse(context)

@csrf_exempt
def subscribed_opportunities_view(request):
    subscribed_opportunities = []

    for subscription in Subscription.objects.filter(user=request.user):
        for opportunity in Opportunity.objects.filter(company=subscription.company):
            serialized_opportunity = {}

            serialized_opportunity['id'] = opportunity.id
            serialized_opportunity['title'] = opportunity.title
            serialized_opportunity['job_type'] = opportunity.job_type
            serialized_opportunity['deadline'] = opportunity.deadline
            serialized_opportunity['company'] = {
                'name': opportunity.company.name,
                'picture': opportunity.company.picture.url,
            }

            try:
                Favourate.objects.get(user=request.user, opportunity=opportunity)
                serialized_opportunity['is_favourate'] = True
            except Favourate.DoesNotExist:
                serialized_opportunity['is_favourate'] = False

            subscribed_opportunities.append(serialized_opportunity)

    return JsonResponse({'data': subscribed_opportunities})


@require_http_methods(["POST"])
def favourate_pressed_view(request, opportunity_id):
    try:
        opportunity = Opportunity.objects.get(id=opportunity_id)
    except Opportunity.DoesNotExist:
        return JsonResponse({'err': 'opportunity does not exits'})

    try:
        Favourate.objects.get(user=request.user, opportunity=opportunity).delete()
    except Favourate.DoesNotExist:
        Favourate.objects.create(user=request.user, opportunity=opportunity)

    return JsonResponse({'status': 'success'})


def favourate_opportunities_view(request):
    favourate_opportunities = []

    for favourate in Favourate.objects.filter(user=request.user):
        favourate_opportunities.append({
            'id': favourate.opportunity.id,
            'title': favourate.opportunity.title,
            'job_type': favourate.opportunity.job_type,
            'deadline': favourate.opportunity.deadline,
            'company': {
                'name': favourate.opportunity.company.name,
                'picture': favourate.opportunity.company.picture.url,
            },
            'is_favourate': True,
        })

    return JsonResponse({'data': favourate_opportunities})


# ????????????????????????????????????????
# @permission_classes([IsAuthenticated])
# @api_view(['GET', 'POST'])
# def company_list(request):
#     if request.method == 'GET':
#         companies = Company.objects.all()
#         serializer = CompanySerializer(companies, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = CompanySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompaniesAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, ]
    search_fields = ['name', ]


@api_view(['GET', 'PUT', 'DELETE'])
def company_detail(request, company_id):
    try:
        companies = Company.objects.get(id=company_id)
    except Company.DoesNotExist as e:
        return Response({'error': str(e)})
    if request.method == 'GET':
        serializer = CompanySerializer(companies)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CompanySerializer(instance=companies, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})

    elif request.method == 'DELETE':
        companies.delete()
        return Response({'deleted': True})


@api_view(['GET'])
def opportunities_by_company(request, company_id):
    try:
        companies = Company.objects.get(id=company_id)
    except Company.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        opportunities = companies.opportunities.all()
        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data)


def subscribe_pressed_view(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return JsonResponse({'error': 'company does not exists'})

    try:
        Subscription.objects.get(user=request.user, company=company).delete()
    except Subscription.DoesNotExist:
        Subscription.objects.create(user=request.user, company=company)

    return JsonResponse({'status': 'success'})


def subscribed_companies_list(request):
    subscribed_companies = []

    for company in Subscription.objects.filter(user=request.user):
        subscribed_companies.append({
            'id': company.company.id,
            'name': company.company.name,
            'about_company': company.company.about_company,
            'read_more': company.company.read_more,
            'is_subscribed': True,
            'picture':company.company.picture,
        })

    return JsonResponse({'data': subscribed_companies})


def all_opportunities_view(request):
    opportunities = []

    for opportunity in Opportunity.objects.all():
        is_favourate = request.user.id != None and (len(Favourate.objects.filter(user=request.user, opportunity=opportunity)) > 0)
        job_category = {
            'id': opportunity.job_category.id,
            'title': opportunity.job_category.title,
        } if opportunity.job_category else None

        opportunities.append({
            'id': opportunity.id,
            'title': opportunity.title,
            'job_type': opportunity.job_type,
            'deadline': opportunity.deadline,
            'company': {
                'name': opportunity.company.name,
                'picture': opportunity.company.picture.url,
            },
            'is_favourate': is_favourate,
            'job_category': job_category,
        })

    return JsonResponse({'data': opportunities})


def all_job_categories_view(request):
    categories = []

    for category in JobCategory.objects.all():
        categories.append({
            'id': category.id,
            'title': category.title,
            })

    return JsonResponse({'data': categories})


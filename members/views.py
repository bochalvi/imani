from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
        'mymembers': mymembers,
        'mymembers_count': Member.objects.count(),
    }
    return HttpResponse(template.render(context, request))


@login_required
def details(request, slug):
    mymember = Member.objects.get(slug=slug)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))


@login_required
def home(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())


def testing(request):
    mydata = Member.objects.all().values()
    template = loader.get_template('template.html')
    context = {
        'mymembers': mydata,
    }
    return HttpResponse(template.render())


@login_required
def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

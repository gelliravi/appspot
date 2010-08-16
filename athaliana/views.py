from django.http import HttpResponse
from django.shortcuts import render_to_response
from bao.athaliana.models import Syntelog
from django.utils import simplejson as json

outgroups = ["lyrata", "papaya", "peach", "grape"]

# Create your views here.
def index(request):
    params = {
            'outgroups': outgroups,
            }
    output = render_to_response('index.html', params)
    return output 


# the core query
def query(request):
    gid = request.GET.get('gid', '').upper().strip()
    if gid:
        if gid.startswith('AT'):
            query = Syntelog.objects.filter(athaliana__iexact=gid)
        else:
            query = Syntelog.objects.filter(description__istartswith=gid)
    else:
        query = Syntelog.objects.all()
        for o in outgroups:
            term = request.GET.get(o, 'A')
            if term=='A': continue
            query = query.filter(**{o+'_code': term})

    query = query.order_by('athaliana')[:10]

    params = {
            'gid': gid,
            'response': query,
            'outgroups': outgroups,
            }
    output = render_to_response('index.html', params)
    return output


# autocomplete for tha athaliana gene id
def autocomplete(request):
    term = request.GET.get('term', '').strip()
    query = Syntelog.objects.filter(athaliana__istartswith=term)\
            .order_by('athaliana')[:5] 
    suggestions = [q.athaliana for q in query]

    return HttpResponse(json.dumps(suggestions))


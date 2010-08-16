from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson as json

from bao.athaliana.models import Syntelog

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
    gid = request.GET.get('gid', '').strip()
    if gid:
        if gid.upper().startswith('AT'):
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
    
    if query.count()==1:
        img = 'simple.png?gid=%s' % query[0].athaliana
        params.update(img=img)

    output = render_to_response('index.html', params)
    return output


# autocomplete for tha athaliana gene id
def autocomplete(request):
    term = request.GET.get('term', '').strip()
    query = Syntelog.objects.filter(athaliana__istartswith=term)\
            .order_by('athaliana')[:5] 
    suggestions = [q.athaliana for q in query]

    return HttpResponse(json.dumps(suggestions))


# plotting
def simple(request):
    gid = request.GET.get('gid', '').strip()
    import random
    import os
    import datetime
    
    os.environ['MPLCONFIGDIR'] = '/tmp'
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.set_title(gid)
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response


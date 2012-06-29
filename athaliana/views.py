from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.core.paginator import Paginator
from django.db.models import Count

from bao.athaliana.models import Syntelog


def get_families():
    q = Syntelog.objects.values(description_key).annotate(num_genes=Count('id'))
    return sorted([x[description_key] for x in q if x["num_genes"] >= 10],
            key=lambda x: x.lower())

outgroups = ["lyrata", "papaya", "poplar", "grape"]
description_key = "description"
families = get_families()


# Create your views here.
def index(request):
    # retrieve the gene families first
    params = {
            'outgroups': outgroups,
            'page_template': "search.html",
            'families': families,
            }
    output = render_to_response('index.html', params)
    return output 


def methods(request):
    params = {
            'page_template': "methods.html",
            }
    output = render_to_response('index.html', params)
    return output 


def contact(request):
    params = {
            'page_template': "contact.html",
            }
    output = render_to_response('index.html', params)
    return output 


# the core query
def query(request):
    gid = request.GET.get('gid', '').strip()
    query_dict = request.GET.copy()
    if 'page' in query_dict: 
        query_dict.pop('page')
    query_str = query_dict.urlencode()
    query = Syntelog.objects.all()

    if gid:
        if gid.upper().startswith('AT') and gid[3] in 'gG': # e.g. AT5G54690
            query = query.filter(athaliana__iexact=gid)
        else:
            #query = query.filter(description__icontains=gid)
            query = query.filter(description__icontains=gid)

    for o in outgroups:
        term = request.GET.get(o, 'A')
        if term=='A': continue
        d = {o+'_code': 'S'}
        if term=='S':
            query = query.filter(**d)
        else:
            query = query.exclude(**d)

    all_query = query.order_by('athaliana')
    counts = all_query.count()
    paginator = Paginator(all_query, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError: 
        page = 1

    try:
        query = paginator.page(page)
    except (EmptyPage, InvalidPage):
        query = paginator.page(paginator.num_pages)

    params = {
            'gid': gid,
            'response': query,
            'outgroups': outgroups,
            'counts': counts,
            'query_str': query_str,
            'page_template': "search.html",
            'families': families,
            }
    
    if counts==1:
        params.update(single=query.object_list[0])

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
    query = Syntelog.objects.filter(athaliana=gid)
    q = query[0]

    import os
    os.environ['MPLCONFIGDIR'] = '/tmp'
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    #_ = lambda x: r"$\mathsf{%s}$" % (x.replace(" ", r"\ "))
    _ = lambda x: x 
    
    fig = Figure()
    root = fig.add_axes([0,0,1,1], axisbg='beige')

    # data
    species = ["athaliana"] + outgroups
    genes = [q.athaliana] + [getattr(q, x+'1') for x in species[1:]]
    codes = [getattr(q, x+'_code') for x in outgroups]
    
    # plot params
    lw = 5
    ms = 12
    size = 12

    # taxa labels
    ytop = .9
    yinterval = .075
    nodes = []
    for s, g, code in zip(species, genes, ['S'] + codes):
        c = 'k' if code=='S' else 'lightgrey'
        root.text(.8, ytop+.01, _(g), ha='center', color=c, size=size)
        root.text(.8, ytop-.01, _(s), ha='center', va='top', color=c, size=size,
                fontstyle='italic')
        nodes.append((.7, ytop))
        ytop -= 2 * yinterval
    
    # tree
    xstart = .7
    xinterval = .6 / 5
    labels = (("rosids", 108),
              ("rosid I+II", 104),
              ("Brassicales", 68),
              ("Arabidopsis", 5)
    )
    ytop = .9
        
    # scales
    xstart = .1
    xx = []
    for label, div in labels:
        xstart += xinterval
        xx.append(xstart)
        root.text(xstart, .2-.01, _("%s (%dmya)" % (label, div)), color="g", 
                    rotation=20, ha='right', va='top', size=size)
    root.plot((.1,.7), (.2,.2), ':', color='gray', lw=lw)
    root.plot(xx, [.2] * len(xx), "go", mec="g", mfc="w", mew=lw, ms=ms)
            
    def draw_branches(n1, n2, height, c1='k', c2='grey', label=''):
        x1, y1 = n1
        x2, y2 = n2
        half_y = .5 * (y1 + y2)
        cnode = (height, half_y)
        root.plot((x1, height), (y1, y1), '-', color=c1, lw=lw)
        root.plot((x2, height), (y2, y2), '-', color=c2, lw=lw)       
        root.plot((height, height), (y1, half_y), '-', color=c1, lw=lw)
        root.plot((height, height), (y2, half_y), '-', color=c2, lw=lw)
        # the synteny code on the corner of branches
        root.text(height-.01, y2+.01, _(label), color=c2, size=size, ha="right")
        return cnode
    
    # draw the tree branches recursively
    node = nodes[0]
    internal_nodes = []
    for i, (x, code) in enumerate(reversed(zip(xx, reversed(codes)))):
        c = 'k' if code=='S' else 'lightgrey'
        node = draw_branches(node, nodes[i+1], x, c2=c, label=code)
        internal_nodes.append(node)
        
    # common ancestral branch
    x, y = node
    root.plot((.1, x), (y, y), 'k-', lw=lw)
    x, y = zip(*internal_nodes)
    root.plot(x, y, 'o', mfc='w', mec='k', mew=lw, ms=ms)
    
    # legends
    root.text(.5, .95, _("Positional history for gene %s" % q.athaliana), 
            ha="center", va="center", size=size, fontweight='bold')
    root.set_xlim((0,1))
    root.set_ylim((0,1))
    root.set_axis_off()
    
    # print out
    canvas = FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_figure(response, format="png")

    return response


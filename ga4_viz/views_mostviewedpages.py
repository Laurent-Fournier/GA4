from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

from django.db.models import Func, Value, Sum
from .models import GaPagesActiveusers

from .color_class import Color



# ------------------------------------------
# Actives Users by page witih query string
# ------------------------------------------
def page(request):
    
    # Traffic sources
    pages = {}
    rows = GaPagesActiveusers.objects.raw("""
        SELECT id, pagePathPlusQueryString, activeUsers
        FROM ga_pages_activeusers
        WHERE account_id = 1 and activeUsers > 2
        ORDER BY activeUsers DESC
    """)
    for row in rows:
        pages[ row.pagepathplusquerystring[0:50] ] = row.activeusers
          
    return render(
        request,
        'page.html',
        {   
            'graphs': [
                {
                    'type': 'TABLE',
                    'title': 'Pages (with Query strings)',
                    'table_titles': {1:'id', 2:'page'},
                    'table_values': pages,
                },
            ],
        }
    )

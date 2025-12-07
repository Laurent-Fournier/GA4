from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

from django.db.models import Func, Value, Sum
from .models import GaDeviceCategory

from .color_class import Color
from .line_class import Line


# ------------------------------------------
# Actives Users by Device 
#  ------------------------------------------
def page(request):
    
    # Devices
    myLine = Line(1, GaDeviceCategory, 'ga_device_category', 'deviceCategory', 'activeUsers', {'date_min': None, 'metric_min': None } )
    deviceCategories = myLine.get_dimension_values()
    print(f'deviceCategory: {deviceCategories}')
    quit()
    
    
    rows = GaPagesActiveusers.objects.raw("""
        SELECT id, pagePathPlusQueryString, SUM(activeUsers) AS activeUsers
        FROM ga_pages_activeusers
        WHERE account_id = 1 and activeUsers > 2
        GROUp BY 
        ORDER BY activeUsers DESC
    """)
    for row in rows:
        pages[ row.pagepathplusquerystring[0:50] ] = row.activeusers
    
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
                    'title': 'Les pages les plus vues',
                    'table_titles': {1:'id', 2:'page'},
                    'table_values': pages,
                },
            ],
        }
    )

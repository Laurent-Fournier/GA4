from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

from django.db.models import Func, Value, Sum
from .models import GaDailyTrafficSources

from .color_class import Color



# ------------------------------
# Page Traffic source  by day
# ------------------------------
def page(request):
    
    # Traffic sources
    traffic_sources = {}
    rows = GaDailyTrafficSources.objects.raw("""
        SELECT MIN(id) AS id, sessionDefaultChannelGrouping, SUM(sessions) AS sessions
        FROM ga_daily_traffic_sources
        GROUP BY sessionDefaultChannelGrouping
        ORDER BY SUM(sessions) DESC
    """)
    for row in rows:
        traffic_sources[ row.sessiondefaultchannelgrouping ] = row.sessions
    print(traffic_sources)
    
    # Months
    rows = GaDailyTrafficSources.objects.raw("""
        SELECT MIN(id) AS id, LEFT(date,7) AS month
        FROM ga_daily_traffic_sources
        GROUP BY LEFT(date,7)
        ORDER BY LEFT(date,7) ASC
    """)
    months = []
    for row in rows:
        months.append(row.month)
    last_month = months[-1]
    months = months[0:-1]

    # load palette
    color = Color()  
    
    # init Datasets
    datasets = {}
    i = -1
    for traffic_source in traffic_sources:
        if traffic_source not in datasets:
            i += 1
            datasets[traffic_source] = {
                'label': traffic_source,
                'datas': [],
                'borderColor': color.get_rgba_foreground(i),
                'backgroundColor': color.get_rgba_background(i),
                'fill': 'true',
                'borderWidth': 2,
                'stack': 'stack1'
            }
            
    #fill datasets            
    rows = GaDailyTrafficSources.objects.raw("""
        SELECT MIN(id) AS id, LEFT(date,7) AS month, sessionDefaultChannelGrouping, SUM(sessions) AS sessions
        FROM ga_daily_traffic_sources
        GROUP BY LEFT(date,7), sessionDefaultChannelGrouping
        ORDER BY LEFT(date,7) ASC
    """)
    for row in rows:
        datasets[ row.sessiondefaultchannelgrouping ]['datas'].append(int(row.sessions))  # add value

    # return HttpResponse(f"[DEBUG] Datasets keys: {datasets.keys()} Count: {len(datasets.keys())}")
    # return HttpResponse(f"[DEBUG] Datasets['Direct']['datas']) : {datasets['Direct']['datas']}")
    datasets_tab = list(datasets.values())
    # return HttpResponse(f"[DEBUG] Datasets_tab: {datasets_tab}")
          
    return render(
        request,
        'page.html',
        {   
            'graphs': [
                {
                    'type': 'LINE',
                    'title': 'Sources de trafic',
                    'labels': months,
                    'datasets': datasets_tab,
                    'raw_data': list(traffic_sources),
                },
            ],
        }
    )

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

from django.db.models import Func, Value, Sum
from .models import GaSource

from .color_class import Color


# ---------------------------
# Page SessionSource by day
# ---------------------------
def page(request):
    
    # Months
    rows = GaSource.objects.raw("""
        SELECT MIN(id) AS id, LEFT(date,7) AS month
        FROM ga_source
        GROUP BY LEFT(date,7)
        ORDER BY LEFT(date,7) ASC
    """)
    months = []
    for row in rows:
        months.append(row.month)
        
    last_month = months[-1]
    months = months[0:-1]
    
    # Active Users by month and Session source
    sql = f"""
        SELECT
            MIN(id) AS id, 
            LEFT(date,7) AS month, 
            CASE
                WHEN sessionSource IN ('google', 'google.com', 'translate.google.com', 'translate.google.fr')
                    THEN 'google'
                WHEN sessionSource IN ('ig', 'l.instagram.com')
                    THEN 'instagram'
                WHEN sessionSource LIKE '%%yahoo%%'
                    THEN 'yahoo'
                WHEN sessionSource LIKE '%%facebook%%'
                    THEN 'facebook'
                ELSE sessionSource
            END AS sessionSource,
            SUM(activeusers) AS activeusers
        FROM ga_source
        WHERE LEFT(date,7) < '{last_month}'
        GROUP BY
            LEFT(date,7), 
            CASE
                WHEN sessionSource IN ('google', 'google.com', 'translate.google.com', 'translate.google.fr')
                    THEN 'google'
                WHEN sessionSource IN ('ig', 'l.instagram.com')
                    THEN 'instagram'
                WHEN sessionSource LIKE '%%yahoo%%'
                    THEN 'yahoo'
                WHEN sessionSource LIKE '%%facebook%%'
                    THEN 'facebook'
                ELSE sessionSource
            END
        ORDER BY
            LEFT(date,7) ASC, sessionsource, activeusers
    """
    rows = GaSource.objects.raw(sql)
    session_sources = {}
    for row in rows:
        # Session sources
        if row.sessionsource not in session_sources:
            session_sources[row.sessionsource] = 0
        session_sources[row.sessionsource] += int(row.activeusers)

    sorted_items = sorted(session_sources.items(), key=lambda x: x[1], reverse=True)
    session_sources = dict(sorted_items)
    
    # les 10 premières sources
    session_sources10 = {}
    for i, (k, v) in enumerate(session_sources.items()):
        if i < 10:
            session_sources10[k] = v
        else:
            break

    # load palette
    color = Color()    

    datasets = []
    i = -1
    for session_source in session_sources10.keys():
        i +=1
        
        datas = []
        for row in rows:
            if row.sessionsource == session_source:
                datas.append(int(row.activeusers))
        
        dataset = {
            'label': session_source,
            'datas': datas,
            'borderColor': color.get_rgba_foreground(i),
            'backgroundColor': color.get_rgba_background(i),
            'fill': 'true',
            'borderWidth': 2,
            'stack': 'stack1'
          }
        datasets.append(dataset)

    dataset = []
    foreground_colors = []
    background_colors = []
    i = -1
    last_month = months[-1]
    for session_source in session_sources10.keys():
        i +=1
        for row in rows:
            if row.sessionsource == session_source and row.month == last_month:
                dataset.append(int(row.activeusers))
        foreground_colors.append(color.get_rgba_foreground(i))
        background_colors.append(color.get_rgba_background(i))
        

    return render(
        request,
        'page.html',
        {   
            'graphs': [
                {
                    'type': 'LINE',
                    'title': 'Sources',
                    'labels': months,
                    'datasets': datasets,
                    'sql': sql,
                    'raw_data': session_sources10,
                },
                {
                    'type': 'PIE',
                    'title': f'Répartition des Sources ({last_month})',
                    'labels': list(session_sources10.keys()),
                    'dataset': dataset,
                    'foreground_colors': foreground_colors,
                    'background_colors': background_colors,
                    'raw_data': session_sources10,
                }
            ],
        }
    )

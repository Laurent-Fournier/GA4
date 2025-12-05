from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

from django.db.models import Func, Value, Sum
from .models import GaSource

# ------------
# Robots.txt
# ------------
def robots_txt(request):
    robots_content = '''
      User-agent: * 
      Disallow: /
      '''
    return HttpResponse(robots_content, content_type="text/plain")

def get_color_palette():
    return [
        {'r': 82, 'g': 138, 'b': 188},
        {'r':108, 'g': 151, 'b': 105},
        {'r':166, 'g':  62, 'b':  64},
        {'r':149, 'g': 203, 'b': 227},
        {'r':217, 'g': 143, 'b':  96},
        {'r':235, 'g': 208, 'b': 127},
        {'r': 40, 'g':  90, 'b': 200},
        {'r': 30, 'g':  70, 'b': 180},
        {'r': 20, 'g':  50, 'b': 160},
        {'r': 10, 'g':  30, 'b': 140},
        {'r':130, 'g': 160, 'b': 240},
        {'r':150, 'g': 180, 'b': 230},
        {'r':170, 'g': 200, 'b': 220},
        {'r':190, 'g': 220, 'b': 210},
        {'r':210, 'g': 230, 'b': 200},
        {'r':140, 'g': 150, 'b': 245},
        {'r':160, 'g': 170, 'b': 235},
        {'r':180, 'g': 190, 'b': 225},
        {'r':200, 'g': 210, 'b': 215},
        {'r':220, 'g': 230, 'b': 205}
    ]

def rename_session(session_source):
    if 'facebook' in session_source :
        session_source = 'facebook'
    elif 'yahoo' in session_source :
            session_source = 'yahoo'
    elif session_source in ['google', 'google.com', 'translate.google.com', 'translate.google.fr']:
            session_source = 'google'
    elif session_source in ['ig', 'l.instagram.com']:
        session_source = 'instagram'
    elif session_source in ['ecosia.org']:
        session_source = 'ecosia'
    elif session_source in ['qwant.com']:
        session_source = 'qwant'
    elif session_source in ['chatgpt.com']:
        session_source = 'chatgpt'
    elif session_source in ['search.lilo.org']:
        session_source = 'lilo'
    elif session_source in ['search.brave.com']:
        session_source = 'brave'
    return session_source

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

    # read palette
    palette = get_color_palette()    

    datasets = []
    i=-1
    for session_source in session_sources10.keys():
        i +=1
        
        datas = []
        for row in rows:
            if row.sessionsource == session_source:
                datas.append(int(row.activeusers))
        
        dataset = {
            'label': session_source,
            'datas': datas,
            'borderColor': f'rgba({palette[i]['r']},{palette[i]['g']},{palette[i]['b']},1)',
            'backgroundColor': f'rgba({palette[i]['r']},{palette[i]['g']},{palette[i]['b']},0.25)',
            'fill': 'true',
            'borderWidth': 2,
            'stack': 'stack1'
          }
        datasets.append(dataset)
        
    return render(
        request,
        'page.html',
        {   
            'title': 'Session Source by month',
            'months': months,
            'session_sources': session_sources10,
            'datasets': datasets,
            'sql': sql,
        }
    )

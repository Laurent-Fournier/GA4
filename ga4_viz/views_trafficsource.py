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
        WHERE date>='2024-09-05'
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
        WHERE date>='2024-09-05'
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
            
    # fill datasets            
    rows = GaDailyTrafficSources.objects.raw("""
        SELECT MIN(id) AS id, LEFT(date,7) AS month, sessionDefaultChannelGrouping, SUM(sessions) AS sessions
        FROM ga_daily_traffic_sources
        WHERE date>='2024-09-05'
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
                    'description': """
                    <ul>
                    <li><strong>Organic search:</strong> Trafic provenant des résultats non payants des moteurs de recherche (Google, Bing, Yahoo, etc). &rarr; Efficacité du référencement naturel (SEO)</li>
                    <li><strong>Direct:</strong> Trafic où l’utilisateur arrive sur ton site en tapant directement l’URL dans la barre d’adresse, ou via un signet (favoris). &rarr; notorité de ta marque ou la fidélité des visiteurs</li>
                    <li><strong>Organic social:</strong> Trafic provenant des réseaux sociaux (Facebook, Twitter, LinkedIn, Instagram, etc.) sans publicité payante.. &rarr; engagement organique sur tes réseaux sociaux.</li>
                    <li><strong>Referral:</strong> Trafic provenant d’un lien sur un autre site web &rarr; partenariats, backlinks ou mentions externes efficaces.</li>
                    <li><strong>Unassigned:</strong> Trafic que Google Analytics ne parvient pas à attribuer à une source spécifique.</li>
                    <li><strong>Organic Video:</strong> Trafic provenant de plateformes vidéo (YouTube, Vimeo, etc.) via des résultats de recherche ou des suggestions non payants. &rarr; impact de ton contenu vidéo.</li>
                    <li><strong>Paid Search:</strong> Trafic provenant des annonces payantes sur les moteurs de recherche (Google Ads, Bing Ads). &rarr; retour sur investissement (ROI) de tes campagnes publicitaires.</li>
                    </ul>
                    """
                },
            ],
        }
    )

from django.shortcuts import render
from django.http import HttpResponse

from .models import GaDailyMetrics, GaDailyTrafficSources, GaDeviceCategory, GaSource
from .lines_class import Lines
from .line_class import Line


# ------------
# Robots.txt
# ------------
def robots_txt(request):
    robots_content = '''
      User-agent: * 
      Disallow: /
      '''
    return HttpResponse(robots_content, content_type="text/plain")


# --------
# Index
# --------
def index(request):
    
    return render(
        request,
        'page.html',
        {}
    )
    


# ------------------------------------
# Monthly stats
# ------------------------------------
def monthly(request):
    
    active_users = Line(
        account_id=1, 
        model = GaDailyMetrics, 
        agregation_function = 'SUM', 
        table = 'ga_daily_metrics', 
        metric = 'activeUsers', 
        filter = {'date_min': '2024-05-01', 'metric_min': 0},
        color_index = 0,
    )
    average_session_duration = Line(
        account_id=1, 
        model = GaDailyMetrics, 
        agregation_function = 'AVG', 
        table = 'ga_daily_metrics', 
        metric = 'averageSessionDuration', 
        filter = {'date_min': '2024-05-01', 'metric_min': 0},
        color_index = 1,
    )
    average_bounce_rate = Line(
        account_id=1, 
        model = GaDailyMetrics, 
        agregation_function = 'AVG', 
        table = 'ga_daily_metrics', 
        metric = 'bounceRate', 
        filter = {'date_min': '2024-05-01', 'metric_min': 0},
        color_index = 2,
    )
    average_screen_page_view_per_session = Line(
        account_id=1, 
        model = GaDailyMetrics, 
        agregation_function = 'AVG', 
        table = 'ga_daily_metrics', 
        metric = 'screenPageViews', 
        filter = {'date_min': '2024-05-01', 'metric_min': 0},
        color_index = 3,
    )
          
    return render(
        request,
        'page.html',
        {   
            'graphs': [
                {
                    'code': 'active_users',
                    'type': 'LINE',
                    'title': 'Utilisateurs actifs mensuels',
                    'labels': active_users.get_months(),
                    'datasets':  active_users.get_datasets(),
                    'description': None
                },                {
                    'code': 'average_session_duration',
                    'type': 'LINE',
                    'title': 'Durée moyenne mensuelle d\'une session',
                    'labels': average_session_duration.get_months(),
                    'datasets':  average_session_duration.get_datasets(),
                    'description': None
                },
                {
                    'code': 'bounce_rate',
                    'type': 'LINE',
                    'title': 'Taux de rebond moyen mensuel',
                    'labels': average_bounce_rate.get_months(),
                    'datasets':  average_bounce_rate.get_datasets(),
                    'description': None
                },                
                {
                    'code': 'screen_page_views_per_user',
                    'type': 'LINE',
                    'title': 'Pages vues par utilisateur moyennes mensuelle',
                    'labels': average_screen_page_view_per_session.get_months(),
                    'datasets':  average_screen_page_view_per_session.get_datasets(),
                    'description': None
                },                
            ],
        }
    )


# ------------------------------------
# Monthly sessions per Traffic source
# ------------------------------------
def trafficsources(request):
    
    myLine = Lines('ABSOLUTE', 1, GaDailyTrafficSources, 'SUM', 'ga_daily_traffic_sources', 'sessionDefaultChannelGrouping', 'sessions', {'date_min': '2024-09-05', 'metric_min': 5}, None )
    myLinePercent = Lines('PERCENT', 1, GaDailyTrafficSources, 'SUM', 'ga_daily_traffic_sources', 'sessionDefaultChannelGrouping', 'sessions', {'date_min': '2024-09-05', 'metric_min': 5}, None )
          
    return render(
        request,
        'page.html',
        {
            'graphs': [
                {
                    'code': 'sourcestraffic_absolute',
                    'type': 'LINES',
                    'title': 'Sessions mensuelles par Source de traffic',
                    'dimensions': myLine.get_dimensions(),
                    'labels': myLine.get_months(),
                    'datasets':  myLine.get_datasets(),
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
                {
                    'code': 'sourcestraffic_percent',
                    'type': 'LINES',
                    'title': 'Pourcentage par Source de traffic',
                    'dimensions': myLinePercent.get_dimensions(),
                    'labels': myLinePercent.get_months(),
                    'datasets':  myLinePercent.get_datasets(),
                    'description': None
                },
            ],
        }
    )


# --------------------------------------
# Monthly sessions per Traffic source
# --------------------------------------
def sources(request):
    
    # sql = f"""
    #     SELECT
    #         MIN(id) AS id, 
    #         LEFT(date,7) AS month, 
    #         CASE
    #             WHEN sessionSource IN ('google', 'google.com', 'translate.google.com', 'translate.google.fr')
    #                 THEN 'google'
    #             WHEN sessionSource IN ('ig', 'l.instagram.com')
    #                 THEN 'instagram'
    #             WHEN sessionSource LIKE '%%yahoo%%'
    #                 THEN 'yahoo'
    #             WHEN sessionSource LIKE '%%facebook%%'
    #                 THEN 'facebook'
    #             ELSE sessionSource
    #         END AS sessionSource,
    #         SUM(activeusers) AS activeusers
    #     FROM ga_source
    #     WHERE LEFT(date,7) < '{last_month}'
    #     GROUP BY
    #         LEFT(date,7), 
    #         CASE
    #             WHEN sessionSource IN ('google', 'google.com', 'translate.google.com', 'translate.google.fr')
    #                 THEN 'google'
    #             WHEN sessionSource IN ('ig', 'l.instagram.com')
    #                 THEN 'instagram'
    #             WHEN sessionSource LIKE '%%yahoo%%'
    #                 THEN 'yahoo'
    #             WHEN sessionSource LIKE '%%facebook%%'
    #                 THEN 'facebook'
    #             ELSE sessionSource
    #         END
    #     ORDER BY
    #         LEFT(date,7) ASC, sessionsource, activeusers
    # """    
    
    myLine = Lines('ABSOLUTE', 1, GaSource, 'SUM', 'ga_source', 'sessionSource', 'activeUsers', 
                  {'date_min': None, 'metric_min': 0}, 
                  {
                      'google': ['google.com', 'translate.google.com', 'translate.google.fr'],
                      'facebook' : ['facebook.com', 'l.facebook.com', 'm.facebook.com', 'lm.facebook.com'],
                      'instagram' : ['l.instagram.com', 'ig'],
                      'yahoo' : ['yahoo', 'fr.search.yahoo.com', 'uk.search.yahoo.com', 'it.search.yahoo.com', 'qc.search.yahoo.com', 'ca.search.yahoo.com'],
                  }
    )
    myLinePercent = Lines('PERCENT', 1, GaSource, 'SUM', 'ga_source', 'sessionSource', 'activeUsers', 
                  {'date_min': None, 'metric_min': 0}, 
                  {
                      'google': ['google.com', 'translate.google.com', 'translate.google.fr'],
                      'facebook' : ['facebook.com', 'l.facebook.com', 'm.facebook.com', 'lm.facebook.com'],
                      'instagram' : ['l.instagram.com', 'ig'],
                      'yahoo' : ['yahoo', 'fr.search.yahoo.com', 'uk.search.yahoo.com', 'it.search.yahoo.com', 'qc.search.yahoo.com', 'ca.search.yahoo.com'],
                  }
    )
          
    return render(
        request,
        'page.html',
        {
            'graphs': [
                {
                    'code': 'sources_absolute',
                    'type': 'LINES',
                    'title': 'Sessions mensuelles par Source',
                    'dimensions': myLine.get_dimensions(),
                    'labels': myLine.get_months(),
                    'datasets':  myLine.get_datasets(),
                    'description': '',
                },
                {
                    'code': 'source_absolute',
                    'type': 'LINES',
                    'title': 'Pourcentage par Source',
                    'dimensions': myLinePercent.get_dimensions(),
                    'labels': myLinePercent.get_months(),
                    'datasets':  myLinePercent.get_datasets(),
                    'description': '',
                },
            ],
        }
    )
    

# --------------------------------
# Monthly Active Users by Device 
#  -------------------------------
def devices(request):
    
    myLine = Lines('ABSOLUTE', 1, GaDeviceCategory, 'SUM', 'ga_device_category', 'deviceCategory', 'activeUsers', {'date_min': None, 'metric_min': None}, None )
    myLinePercent = Lines('PERCENT', 1, GaDeviceCategory, 'SUM', 'ga_device_category', 'deviceCategory', 'activeUsers', {'date_min': None, 'metric_min': None}, None )
    
    return render(
        request,
        'page.html',
        {   
            'graphs': [
                {
                    'code': 'devices_absolute',
                    'type': 'LINES',
                    'title': 'Utilisateurs actifs mensuels par Device',
                    'dimensions': myLine.get_dimensions(),
                    'labels': myLine.get_months(),
                    'datasets':  myLine.get_datasets(),
                    'description': """
                    <ul>
                    <li><strong>mobile :</strong> Appareils mobiles (smartphones)</li>
                    <li><strong>tablet :</strong> Tablettes</li>
                    <li><strong>desktop :</strong> Ordinateurs de bureau ou portables.</li>
                    </ul>
                    """
                },
                {
                    'code': 'devices_percent',  
                    'type': 'LINES',
                    'title': 'Pourcentage par Device',
                    'dimensions': myLinePercent.get_dimensions(),
                    'labels': myLinePercent.get_months(),
                    'datasets':  myLinePercent.get_datasets(),
                    'description': None
                },
            ],
        }
    )    
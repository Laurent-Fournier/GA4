from django.db import models


class GaAccount(models.Model):
    url = models.CharField(max_length=255, blank=True, null=True)
    analytics_id = models.CharField(max_length=45, blank=True, null=True)
    analytics_name = models.CharField(max_length=45, blank=True, null=True)
    property_id = models.CharField(max_length=45, blank=True, null=True)
    property_name = models.CharField(max_length=45, blank=True, null=True)
    google_tag_id = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ga_account'


class GaDailyMetrics(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    activeusers = models.PositiveIntegerField(db_column='activeUsers', blank=True, null=True)  # Field name made lowercase.
    sessions = models.PositiveIntegerField(blank=True, null=True)
    averagesessionduration = models.FloatField(db_column='averageSessionDuration', blank=True, null=True)  # Field name made lowercase.
    bouncerate = models.FloatField(db_column='bounceRate', blank=True, null=True)  # Field name made lowercase.
    screenpageviews = models.PositiveIntegerField(db_column='screenPageViews', blank=True, null=True)  # Field name made lowercase.
    screenpageviewspersession = models.FloatField(db_column='screenPageViewsPerSession', blank=True, null=True)  # Field name made lowercase.
    screenpageviewsperuser = models.FloatField(db_column='screenPageViewsPerUser', blank=True, null=True)  # Field name made lowercase.
    scrolledusers = models.PositiveIntegerField(db_column='scrolledUsers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ga_daily_metrics'


class GaDailyTrafficSources(models.Model):
    account_id = models.PositiveIntegerField()
    date = models.DateField(blank=True, null=True)
    sessiondefaultchannelgrouping = models.CharField(db_column='sessionDefaultChannelGrouping', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sessions = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ga_daily_traffic_sources'


class GaDeviceCategory(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    devicecategory = models.CharField(db_column='deviceCategory', max_length=255, blank=True, null=True)  # Field name made lowercase.
    activeusers = models.PositiveIntegerField(db_column='activeUsers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ga_device_category'


class GaPagesActiveusers(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    pagepathplusquerystring = models.CharField(db_column='pagePathPlusQueryString', max_length=255, blank=True, null=True)  # Field name made lowercase.
    activeusers = models.PositiveIntegerField(db_column='activeUsers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ga_pages_activeusers'


class GaReferer(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    pagereferrer = models.CharField(db_column='pageReferrer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    activeusers = models.PositiveIntegerField(db_column='activeUsers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ga_referer'


class GaSource(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    sessionsource = models.CharField(db_column='sessionSource', max_length=255, blank=True, null=True)  # Field name made lowercase.
    activeusers = models.PositiveIntegerField(db_column='activeUsers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ga_source'


class JpTurnover(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    month = models.CharField(max_length=45, blank=True, null=True)
    turnover = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jp_turnover'


class Keywords(models.Model):
    keyword = models.CharField(max_length=255, blank=True, null=True)
    family = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keywords'


class PageInfo(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    page = models.CharField(max_length=255, blank=True, null=True)
    word_count = models.PositiveIntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    keywords_count = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'page_info'


class WebsiteBrokenlink(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    broken_link = models.CharField(max_length=255, blank=True, null=True)
    server_response = models.CharField(max_length=45, blank=True, null=True)
    link_text = models.CharField(max_length=255, blank=True, null=True)
    source_page_url = models.CharField(max_length=255, blank=True, null=True)
    source_page_html = models.TextField(blank=True, null=True)
    is_fixed = models.PositiveIntegerField(blank=True, null=True)
    fixed_date = models.DateField(blank=True, null=True)
    new_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_brokenlink'


class WebsiteDatabase(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    value = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_database'


class WebsiteLogbook(models.Model):
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_logbook'


class WebsitePerformance(models.Model):
    account_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    technology = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_performance'


class WebsiteSearchengine(models.Model):
    account_id = models.PositiveIntegerField(blank=True, null=True)
    searchengine = models.CharField(max_length=45, blank=True, null=True)
    display_order = models.PositiveIntegerField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    word_count = models.PositiveIntegerField(blank=True, null=True)
    keywords_count = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_searchengine'
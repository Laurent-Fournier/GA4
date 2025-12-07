from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Func, Value, Sum




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
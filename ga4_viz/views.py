from django.shortcuts import render
from django.http import HttpResponse

# ------------
# Robots.txt
# ------------
def robots_txt(request):
    robots_content = '''
      User-agent: * 
      Disallow: /
      '''
    return HttpResponse(robots_content, content_type="text/plain")

# ------------
# Page
# ------------
def page(request):
    return render(
        request,
        'page.html',
        {}
    )

import urllib.request
import re

url = "https://www.encyclopedia-titanica.org/titanic-victim/john-jacob-astor.html"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    print("MATCHES:", matches[:10])
except Exception as e:
    print(e)

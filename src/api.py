from falcon import API

from project_name.api.urls import urls


app = API()

for url in urls:
    app.add_route(*url)

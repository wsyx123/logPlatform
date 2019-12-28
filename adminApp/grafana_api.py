import requests

def create_grafana_info(url,body):
    url = '/api/admin/users'
    body = {
      "name":"user",
      "email":"user@graf.com",
      "login":"user",
      "password":"user"
    }


def get_dashboards(url,auth):
    res = requests.get(url,auth=auth)
    return res
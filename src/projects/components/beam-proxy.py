from common import Service
from vars import PROXY_ID, KEY
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'ApiKey ' + PROXY_ID + ' ' + KEY
}

services = [
    Service("Beam-Proxy", "beam-proxy-health", "beam.proxy.health.item", "Beam-Proxy: Health", "v1/health", [], 3600, headers, None),
    #Service("Beam-Proxy", "beam-proxy-tasks", "beam.proxy.tasks.item", "Beam-Proxy: Tasks", "/v1/tasks?filter=todo", "text", 36, headers)
]
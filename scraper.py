import requests
from typing import List

URL = "https://zapier.com/api/graphql/v2"

def get_slug_request(name:str) -> dict:
  return {
  "query": f"""
  query Request($name: String = "{name}") {{
    getAppsByNameContains(nameContains: $name, limit: 1,
     excludeUpcoming: false, offset: 0 ) {{
       edges {{ slug name }}
    }}
  }}
  """
}

def get_slug_from_content(content: dict) -> str:
  return content['data']['getAppsByNameContains']['edges'][0]['slug']

def get_zap_slug(name: str) -> str:
  request_body = get_slug_request(name)
  content = requests.post(URL, json=request_body).json()
  return get_slug_from_content(content)


def get_template_request(slug: str) -> dict:
  return {
    "query": f"""
    query Request($slugs: [String!] = ["{slug}"]) {{
       zapTemplatesConnectionV2(serviceSlugs: $slugs, first: 10, orderBy: DEFAULT, mustContainAllServices: true) {{
          totalCount
          edges {{title }}
        }}
      }}""",
  }

def get_template_edges_from_content(content: dict) -> List[str]:
  return content['data']['zapTemplatesConnectionV2']['edges']

def get_zap_templates(slug: str) -> List[str]:
  request_body = get_template_request(slug)
  content = requests.post(URL, json=request_body).json()
  edges = get_template_edges_from_content(content)
  return [edge['title'] for edge in edges]

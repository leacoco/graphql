import json
import requests
from requests.auth import HTTPBasicAuth
import os
import json

def get_repos():
  QUERY = """
  query {{
  rateLimit {{
      cost
      remaining
      resetAt
  }}
  viewer {{
      login
  }}
  search(query: "org:leacoco created:{start}..{end}" type: REPOSITORY first:100 {AFTER}) {{
      pageInfo {{
      startCursor
      hasNextPage
      endCursor
      }}
      repositoryCount
      repos: edges {{
      repo: node {{
          ... on Repository {{
          name
          object(expression: "master:.circleci") {{
              id
          }}
          }}
      }}
      }}
  }}
  }}
  """

  result = []

  import datetime
  end = datetime.datetime.now().date()

  while True:
      after = ""
      start = end - datetime.timedelta(days=180)
      if start.year < 2018:
          break
      while True:
          print("Page: {after}".format(after=after))
          response = requests.post(
              "https://api.github.com/graphql",
              headers={
                  "Authorization": f"bearer {os.getenv('GITHUB_TOKEN')}"
              },
              data=json.dumps({
                  "query": QUERY.format(AFTER=after, start=start, end=end)
              })
          )
          print(response.json())
      #     data = response.json()["data"]
      #     repos = data["search"]["repos"]
      #     for repo in repos:
      #         if repo["repo"]["object"] is not None:
      #             result.append(repo["repo"]["name"])
      #     has_next_page = data["search"]["pageInfo"]["hasNextPage"]
      #     if not has_next_page:
      #         break
      #     after = "after: \"{cursor}\"".format(
      #         cursor=data["search"]["pageInfo"]["endCursor"],
      #     )
      # end = start

  return result


if __name__ == '__main__':
  print(get_repos())

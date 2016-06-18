# coding: utf-8

import httplib, urllib, json, os

def post_message(message):
  token = "slack-token"
  channel_id = "channel_id"
  conn = httplib.HTTPSConnection("slack.com")
  params = urllib.urlencode({ "token" : token, "channel": channel_id, "text": message, "pretty": 1 })
  conn.request("GET", "/api/chat.postMessage?%s" % params)
  response = conn.getresponse()
  data = json.loads(response.read())
  print data

def check_branch(data, base_branch_name, allow_branch_name):
  if data[0]["base"]["ref"] == base_branch_name:
    if data[0]["head"]["ref"] != allow_branch_name:
      message = { "base_branch": data[0]["head"]["ref"], "head_branch": data[0]["head"]["ref"], "message" : "not required!" }
    else:
      message = { "base_branch": data[0]["head"]["ref"], "head_branch": data[0]["head"]["ref"], "message" : "ok" }

    post_message(json.dumps(message, indent=2))

def main():
  conn = httplib.HTTPSConnection("api.github.com")
  headers = {"Authorization": "token %s" % os.getenv("GITHUB_TOKEN"), "User-Agent": ""}
  conn.request("GET", "/repos/:owner/:repo/pulls?sort=updated&direction=desc", headers=headers)
  response = conn.getresponse()
  data = json.loads(response.read())
  check_branch(data, "master", "develop")

if __name__ == "__main__":
  main()

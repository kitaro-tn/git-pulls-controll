# coding: utf-8

import httplib, json, os

def check_branch(data, base_branch_name, allow_branch_name):
  if data[0]["base"]["ref"] == base_branch_name:
    if data[0]["head"]["ref"] != allow_branch_name:
      print data[0]["head"]["ref"]
      print "not required!"
    else:
      print "ok"

def main():
  conn = httplib.HTTPSConnection("api.github.com")
  headers = {"Authorization": "token %s" % os.getenv("GITHUB_TOKEN"), "User-Agent": ""}
  conn.request("GET", "/repos/kitaro-tn/git-flow-study/pulls?sort=updated&direction=desc", headers=headers)
  response = conn.getresponse()
  data = json.loads(response.read())
  check_branch(data, "master", "develop")

if __name__ == "__main__":
  main()

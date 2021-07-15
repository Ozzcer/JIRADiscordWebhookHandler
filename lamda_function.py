import json
import requests

discordWebhookUrl = "PLACEHOLDER" # Discord webhook url
jiraURL = "PLACEHOLDER" # url of JIRA site
userId = "PLACEHOLDER"  # user to ignore when reporting comments
discordBotUsername = "TSJI3000"

def lambda_handler(event, context):
    print(event)
    
    data = {
        "content": "Error with integration, check AWS log for event details",
        "username": discordBotUsername,
    }
    try:
        body = json.loads(event["body"])
        if body["webhookEvent"] == "comment_created":
          issue = body["issue"]
          comment = body["comment"]
          if comment["author"]["accountId"] == userId:
              return
          msgString = "------------------------------\n"
          msgString += "Comment on " + issue["fields"]["summary"] + "\n"
          msgString += jiraURL + \
              issue["key"] + "\n"
          msgString += "Comment author: " + \
              comment["author"]["displayName"] + "\n"
          msgString += "Comment:\n" + comment["body"] + "\n"
          msgString += "------------------------------"
          data["content"] = msgString
          response = requests.post(discordWebhookUrl, json=data)
          return
        elif body["webhookEvent"] == "jira:issue_created":
          try:
            issue = body["issue"]
            msgString = "------------------------------\n"
            msgString += "New issue " + issue["fields"]["summary"] + "\n"
            msgString += jiraURL + \
                issue["key"] + "\n"
            msgString += issue["fields"]["description"] + "\n"
            msgString += "------------------------------"
            data["content"] = msgString
            response = requests.post(discordWebhookUrl, json=data)
            return
          except Exception as e:
            data["content"] = "Error with integration caused by issue created webhook, check AWS log for event details"
            response = requests.post(discordWebhookUrl, json=data)
            raise e
        else:
          data["content"] = "Error, webhook type did not match any expected types, check AWS log for event details"
    except Exception as e:
        response = requests.post(discordWebhookUrl, json=data)
        raise e

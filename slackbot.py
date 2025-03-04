import json
import requests

def post_to_slack(message):
    webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = json.dumps({'text':message})
    response = requests.post(
        webhook_url, data=slack_data,
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

if __name__ == '__main__':
    post_to_slack('hello')

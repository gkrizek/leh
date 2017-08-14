# Notification

Using leh, you can create alerts as soon as an unhandled exception happens. This can be done in many ways, but using [SNS](https://aws.amazon.com/sns/) would be a good solution.

#### leh Configuration:

```
import sys
import leh
leh.Initialize(
    ExecuteLambda=True,
    FunctionName="notification-function"
)
sys.excepthook = leh.Hook
```


#### Notification Lambda Function:

```
import json
import boto3
sns = boto3.client('sns')

def handler(event, context):
  response = client.publish(
    TopicArn='TopicName',
    Message=json.dumps(event)
  )
  return response
```

# Error Log

Using leh, you can create a separate log stream specifically for errors. This makes is much easier to find errors and store them separately than `stdout`. This also makes Lambda logging more like an expected logging structure.

#### leh Configuration:

```
import sys
import leh
leh.Initialize(
    ExecuteLambda=True,
    FunctionName="error-log-function"
)
sys.excepthook = leh.Hook
```


#### Logging Lambda Function:

```
def handler(event, context):
  print(event)
  return
```

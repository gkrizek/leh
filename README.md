# leh

## About

_Lambda Exception Helper_

leh makes it easier to find unhandled exception log entries in [AWS Lambda](https://aws.amazon.com/lambda/) logs.

AWS Lambda logs both `stdout` and `stderr` to the same stream in [CloudWatch](https://aws.amazon.com/cloudwatch/). This can make it difficult to find your error logs amongst all other `stdout` entries. If you don't view your logs immediately after an error is thrown, it gets even harder due to new log streams starting.

leh makes this process easier by adding a message right before all unhandled exception logs. You can then search your logs with the predetermined message and find your exceptions faster.

leh also gives you the ability to execute a separate Lambda function when an unhandled exception occurs. This allows you to either create a separate log file for errors only or take action whenever an unhandled exception occurs.

## Installation

leh can be installed using the pip distribution system for Python by issuing:

```
$ pip install leh
```

Alternatively, you can run use `setup.py` to install by cloning this repository and issuing:

```
$ python setup.py install  # you may need sudo depending on your python installation
```

## Usage

You can start using leh with just 4 lines to your Handler:

```
import sys
import leh
leh.Initialize()
sys.excepthook = leh.Hook
```

This will add a default message of `"leh excepthook executed:"` just before your unhandled exception log.

You can customize your message, as well as setup a Lambda function, by passing parameters to the `Initialize()` function. Possible parameters are:

| Parameter       | Required                         |  Type   | Description                                                   | Default                  |
|-----------------|----------------------------------|---------|---------------------------------------------------------------|--------------------------|
| `Message`       | No                               | String  | Custom message to prepend to unhandled exception logs.        | leh excepthook executed: |
| `ExecuteLambda` | No                               | Boolean | Enable or Disable Lambda execution on error.                  | `False`                  |
| `FunctionName`  | Yes if `ExecuteLambda` is `True` | String  | Name of the function to execute if `ExecuteLambda` is `True`. | None                     |
| `AWSKey`        | No                               | String  | AWS Access Key for invoking a Lambda function.                | None                     |
| `AWSSecret`     | No                               | String  | AWS Secret Key for invoking a Lambda function.                | None                     |

_I always recommend using [IAM Roles](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) instead of passing in AWS credentials_

#### Performance

Although the `Initialize()` function usually completes in under 100 milliseconds, it's possible to not execute it and use environment variables instead. You can define the the same parameters of the `Initialize()` function using environment variables. The corresponding parameter names to environment variable names as follows:

| Parameter Name  | Environment Variable Name |
|-----------------|---------------------------|
| `Message`       | `LEH_MESSAGE`             |
| `ExecuteLambda` | `LEH_EXECUTE_LAMBDA`      |
| `FunctionName`  | `LEH_FUNCTION_NAME`       |
| `AWSKey`        | `LEH_AWS_KEY`             |
| `AWSSecret`     | `LEH_AWS_SECRET`          |

_WARNING: If you do not call the `Initialize()` function, you MUST define a `LEH_MESSAGE` environment variable._

If you are only appending a custom message to your exception logs there is no delay in exiting. However, if you are executing a Lambda function there will be a slight delay between when the error is thrown and when the error is logged and the program is exited. This delay is the time it takes to execute the Lambda function. We always call the Lambda function asynchronously, so there is never a wait for a response.

## Examples

Create a custom message:

```
import sys
import leh
leh.Initialize(
    Message="My Custom Hook Message"
)
sys.excepthook = leh.Hook
```


Execute a Lambda function:

```
import sys
import leh
leh.Initialize(
    ExecuteLambda=True,
    FunctionName="error-log-function"
)
sys.excepthook = leh.Hook
```

Execute a Lambda function with specific keys:

```
import sys
import leh
leh.Initialize(
    ExecuteLambda=True,
    FunctionName="error-log-function",
    AWSKey="AKIAIOSFODNN7EXAMPLE",
    AWSSecret="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

)
sys.excepthook = leh.Hook
```

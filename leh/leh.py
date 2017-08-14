import boto3
import os
import json
from traceback import format_exception


def ExecuteLambda(Function, Traceback):
    if 'LEH_AWS_KEY' in os.environ and 'LEH_AWS_SECRET' not in os.environ:
        raise Exception("'LEH_AWS_KEY' defined but not 'LEH_AWS_SECRET'")
    elif 'LEH_AWS_KEY' not in os.environ and 'LEH_AWS_SECRET' in os.environ:
        raise Exception("'LEH_AWS_SECRET' defined but not 'LEH_AWS_KEY'")
    elif 'LEH_AWS_KEY' in os.environ and 'LEH_AWS_SECRET' in os.environ:
        awslambda = boto3.client(
            'lambda',
            aws_access_key_id=os.environ['LEH_AWS_KEY'],
            aws_secret_access_key=os.environ['LEH_AWS_SECRET']
        )
    else:
        awslambda = boto3.client('lambda')

    payload = {
        "function": os.environ['AWS_LAMBDA_FUNCTION_NAME'],
        "region": os.environ['AWS_REGION'],
        "origin-log-group": os.environ['AWS_LAMBDA_LOG_GROUP_NAME'],
        "origin-log-stream": os.environ['AWS_LAMBDA_LOG_STREAM_NAME'],
        "exception": Traceback
    }

    response = awslambda.invoke(
        FunctionName=Function,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    return response


def Initalize(
    Message="leh excepthook executed:",
    ExecuteLambda=False,
    FunctionName=None,
    AWSKey=None,
    AWSSecret=None
):
    # Validate Input
    boolean = [True, 'True', 'true', 1, '1', False, 'False', 'false', 0, '0']
    if ExecuteLambda not in boolean:
        raise Exception(
            "'ExecuteLambda' must be a boolean"
        )

    if (ExecuteLambda in [True, 'True', 'true', 1, '1'] and
        FunctionName is None):
        raise Exception(
            "'ExecuteLambda' set to True but 'FunctionName' is not defined"
        )

    if AWSKey is not None and AWSSecret is None:
        raise Exception(
            "'AWSKey' defined but not 'AWSSecret'"
        )
    elif AWSKey is None and AWSSecret is not None:
        raise Exception(
            "'AWSSecret' defined but not 'AWSKey'"
        )

    #Initialize
    os.environ['LEH_MESSAGE'] = Message

    if (ExecuteLambda is not False and
        ExecuteLambda in [True, 'True', 'true', 1, '1']):
        os.environ['LEH_EXECUTE_LAMBDA'] = "True"

    if FunctionName is not None:
        os.environ['LEH_FUNCTION_NAME'] = FunctionName

    if AWSKey is not None:
        os.environment['LEH_AWS_KEY'] = AWSKey

    if AWSSecret is not None:
        os.environment['LEH_AWS_SECRET'] = AWSSecret

    return 'leh successfully initialized'


def Hook(type, value, traceback):
    message = os.environ['LEH_MESSAGE']
    lines = format_exception(type, value, traceback)
    exception = ''.join(lines)
    if ('LEH_EXECUTE_LAMBDA' in os.environ and
        os.environ['LEH_EXECUTE_LAMBDA'] in [True, 'True', 'true', 1, '1']):
        if 'LEH_FUNCTION_NAME' in os.environ:
            function_name = os.environ['LEH_FUNCTION_NAME']
            ExecuteLambda(
                Function=function_name,
                Traceback=exception
            )
        else:
            error = ("'LEH_EXECUTE_LAMBDA' set to 'True'" +
                     " but 'LEH_FUNCTION_NAME' not defined.")
            raise Exception(
                error
            )
    print(message)
    print(exception)

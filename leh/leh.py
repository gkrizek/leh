import boto3
import os
import json
from traceback import format_exception


def ExecuteLambda(Function, Payload):
    if 'LEH_AWS_KEY' in os.environ and 'LEH_AWS_SECRET' in os.environ:
        awslambda = boto3.client(
            'lambda',
            aws_access_key_id=os.environ['LEH_AWS_KEY'],
            aws_secret_access_key=os.environ['LEH_AWS_SECRET']
        )
    else:
        awslambda = boto3.client('lambda')

    response = awslambda.invoke(
        FunctionName=Function,
        InvocationType='Event',
        Payload=json.dumps(Payload)
    )
    return response


def Initalize(
    Message="leh excepthook executed:",
    ExecuteLambda=False,
    FunctionName=None,
    AWSKey=None,
    AWSSecret=None
):



def Hook(type, value, traceback):
    message = os.environ['LEH_MESSAGE']
    lines = format_exception(type, value, traceback)
    exception = ''.join(lines)
    if ('LEH_EXECUTE_LAMBDA' in os.environ and
        os.environ['LEH_EXECUTE_LAMBDA'] in [True, 'True', 'true', 1, '1']):
        if 'LEH_FUNCTION_NAME' in os.environ:
            ExecuteLambda(
                Function=function_name,
                Traceback=exception
            )
        else:
            raise Exception(
                "ExecuteLambda set to 'True' but not FunctionName defined."
            )
    print(message)
    print(exception)

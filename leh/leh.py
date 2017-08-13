import boto3
import os
from traceback import format_exception

def ExecuteLambda(Function):
    if 'LEH_AWS_KEY' in os.environ and 'LEH_AWS_SECRET' in os.environ:
        awslambda = boto3.client(
            'lambda',
            aws_access_key_id=os.environ['LEH_AWS_KEY'],
            aws_secret_access_key=os.environ['LEH_AWS_SECRET']
        )
    else:
        awslambda = boto3.client('lambda')

    response = awslambda.invoke_async(
        FunctionName=Function,
        InvokeArgs=b'bytes'|file
    )
    return response

    
def Initalize():



def Hook(type, value, traceback):
    message = os.environ['LEH_MESSAGE']
    print(message)
    lines = format_exception(type, value, traceback)
    print((''.join(lines))

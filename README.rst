leh
===

|image0| |image1| |image2|

About
-----

*Lambda Exception Helper*

leh makes it easier to find unhandled exception log entries in `AWS
Lambda <https://aws.amazon.com/lambda/>`__ logs.

AWS Lambda logs both ``stdout`` and ``stderr`` to the same stream in
`CloudWatch <https://aws.amazon.com/cloudwatch/>`__. This can make it
difficult to find your error logs amongst all other ``stdout``. If you
don't view your logs immediately after an error is thrown, it gets even
harder due to new log streams starting.

leh makes this process easier by adding a message right before all
unhandled exception logs. You can then search your logs with the
predetermined message and find your exceptions faster.

leh also gives you the ability to execute a separate Lambda function
when an unhandled exception occurs. This allows you to either create a
separate log file for errors only or take action whenever an unhandled
exception occurs.

Installation
------------

leh can be installed using the pip distribution system for Python by
issuing:

::

    $ pip install leh

Alternatively, you can run use ``setup.py`` to install by cloning this
repository and issuing:

::

    $ python setup.py install  # you may need sudo depending on your python installation

Usage
-----

You can start using leh by adding just 2 lines to your Handler:

::

    import leh
    leh.Initialize()

This will add a default message of ``"leh excepthook executed:"`` just
before your unhandled exception log.

You can customize your message, as well as setup a Lambda function, by
passing parameters to the ``Initialize()`` function. Possible parameters
are:

+-------------------+--------------------------------------+---------+--------------------------------------------------------+------------------------------+
| Parameter         | Required                             | Type    | Description                                            | Default                      |
+===================+======================================+=========+========================================================+==============================+
| ``Message``       | No                                   | String  | Custom message to prepend to unhandled exception logs. | ``leh excepthook executed:`` |
+-------------------+--------------------------------------+---------+--------------------------------------------------------+------------------------------+
| ``ExecuteLambda`` | No                                   | Boolean | Enable or Disable Lambda execution on error.           | ``False``                    |
+-------------------+--------------------------------------+---------+--------------------------------------------------------+------------------------------+
| ``FunctionName``  | Yes if ``ExecuteLambda`` is ``True`` | String  | Name of the function to execute.                       | None                         |
+-------------------+--------------------------------------+---------+--------------------------------------------------------+------------------------------+
| ``AWSKey``        | No                                   | String  | AWS Access Key for invoking a Lambda function.         | None                         |
+-------------------+--------------------------------------+---------+--------------------------------------------------------+------------------------------+
| ``AWSSecret``     | No                                   | String  | AWS Secret Key for invoking a Lambda function.         | None                         |
+-------------------+--------------------------------------+---------+--------------------------------------------------------+------------------------------+

I always recommend using `IAM
Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`__

Payload
^^^^^^^

When invoking a Lambda function, everything you need to know is included
in the payload.

*Example Payload:*

::

    {
      "function": "MyFunction",
      "region": "us-west-2",
      "origin-log-group": "/aws/lambda/myfunction",
      "origin-log-stream": "f407a393-50d2-410a-a9c7-45a6a04e506e",
      "exception": "Traceback (most recent call last):\n  File "test.py", line 22, in <module>    print(list[1])\nIndexError: list index out of range"
    }

Performance
^^^^^^^^^^^

If you are only appending a custom message to your exception logs there
is no delay in exiting. However, if you are executing a Lambda function
there will be a slight delay between when the error is thrown and when
the error is logged and the program is exited. This delay is the time it
takes to execute the Lambda function. leh always calls the Lambda
function asynchronously, so there is never a wait for a response.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

Although the ``Initialize()`` function usually completes in under 100
milliseconds, it's possible to not execute it and use environment
variables instead. You can define the the same parameters of the
``Initialize()`` function using environment variables. The corresponding
parameter names to environment variable names as follows:

+---------------------+-----------------------------+
| Parameter Name      | Environment Variable Name   |
+=====================+=============================+
| ``Message``         | ``LEH_MESSAGE``             |
+---------------------+-----------------------------+
| ``ExecuteLambda``   | ``LEH_EXECUTE_LAMBDA``      |
+---------------------+-----------------------------+
| ``FunctionName``    | ``LEH_FUNCTION_NAME``       |
+---------------------+-----------------------------+
| ``AWSKey``          | ``LEH_AWS_KEY``             |
+---------------------+-----------------------------+
| ``AWSSecret``       | ``LEH_AWS_SECRET``          |
+---------------------+-----------------------------+

**Warning:**

-  If you do not call the ``Initialize()`` function, you MUST define a
   ``LEH_MESSAGE`` environment variable.
-  If you do not call the ``Initialize()`` function and choose to use
   environment variables instead, you must manually set the
   ``sys.excepthook`` in your Handler:

::

    import sys
    import leh
    sys.excepthook = leh.Hook

Examples
--------

Create a custom message:

::

    import leh
    leh.Initialize(
        Message="My Custom Hook Message"
    )

Execute a Lambda function:

::

    import leh
    leh.Initialize(
        ExecuteLambda=True,
        FunctionName="error-log-function"
    )

Execute a Lambda function with specific keys:

::

    import leh
    leh.Initialize(
        ExecuteLambda=True,
        FunctionName="error-log-function",
        AWSKey="AKIAIOSFODNN7EXAMPLE",
        AWSSecret="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

    )

.. |image0| image:: https://img.shields.io/pypi/v/leh.svg
.. |image1| image:: https://img.shields.io/circleci/project/github/gkrizek/leh.svg
.. |image2| image:: https://img.shields.io/pypi/l/leh.svg

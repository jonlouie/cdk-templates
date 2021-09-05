import os
from aws_cdk import (
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    core,
)


class TestLambdaCronStack(core.Stack):
    # Since code is "inline", CDK deploys code to an "index.py" file
    DEFAULT_HANDLER_FILE_NAME = "index"

    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        with open(os.path.join("lambda", "handler.py"), encoding="utf8") as handler_file:
            handler_code = handler_file.read()

        lambda_func = lambda_.Function(
            self, "Singleton",
            code=lambda_.Code.inline(handler_code),
            handler=f"{self.DEFAULT_HANDLER_FILE_NAME}.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_8,
        )

        # Run at the top of every hour
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        scheduling_rule = events.Rule(
            self, "Scheduling Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'),
        )
        scheduling_rule.add_target(targets.LambdaFunction(lambda_func))


app = core.App()
TestLambdaCronStack(app, "LambdaCronExample")
app.synth()

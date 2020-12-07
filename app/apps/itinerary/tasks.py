from celery import shared_task

# Just an example of how to use a task


@shared_task
def example_task(text=""):
    # Call the following from anywhere to push this function in the task queue
    # example_task.delay("FOO")
    print(f"Debug Celery task here {text}")

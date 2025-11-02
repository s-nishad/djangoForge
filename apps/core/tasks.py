from celery import shared_task

@shared_task
def test_task():
    print("✅ Celery task executed successfully!")
    return "Task completed"

from UHE.extensions import celery

@celery.task(ignore_result=True)
def clock(word):
    print(word)
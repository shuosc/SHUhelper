from UHE.app import create_app
# from UHE.extensions import celery 

app = create_app()

app.run(host="0.0.0.0", port=4000)
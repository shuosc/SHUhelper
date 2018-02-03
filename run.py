from UHE.app import create_app
import click
import UHE.plugins.SHU_course.manage as manage
# from UHE.extensions import celery 
print('before app start')
app = create_app()

print('app start')
@app.cli.command()
def get_xk_8080():
    manage.get_xk('http://xk.shu.edu.cn:8080/')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
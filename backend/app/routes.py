from app import app
from .forms import FirePut

GETPOST = ['GET', 'POST']

@app.route('/', methods=GETPOST)
@app.route('/index', methods=GETPOST)
def index():
    return "hi"
    '''
    fireform = FirePut()
    if form.validate_on_submit():
        putdata = {'Name' : form.name.data}
    '''    


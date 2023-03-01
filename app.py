from flask import Flask  , render_template , request , url_for , redirect
import os


usercontentfolders = os.path.join(os.getcwd() , 'static' , 'usercontentfolders')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/make-folder' , methods=['POST'])
def makeFolder():
    newFolderName = request.form['new-folder-input']
    if len(newFolderName.strip()) == 0:
        print('no empty folder allowed')
        return redirect(url_for('home'))
    else:
        try:
            os.mkdir(os.path.join(usercontentfolders , newFolderName))
        except  FileExistsError:
            print("This Folder Already exists")
        except Exception:
            print("An error occured")    
    return redirect(url_for('home'))
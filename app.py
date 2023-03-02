from flask import Flask  , render_template , request , url_for , redirect
import os


usercontentfolders = os.path.join(os.getcwd() , 'static' , 'usercontentfolders')
allFolders = os.listdir(usercontentfolders)


app = Flask(__name__)

@app.route("/")
def home():
    allFolders = os.listdir(usercontentfolders)
    return render_template('home.html' , allFolders=allFolders)

@app.route('/make-folder' , methods=['POST'])
def makeFolder():
    newFolderName = request.form['new-folder-input']
    if len(newFolderName.strip()) == 0 or len(newFolderName) > 15:
        print('no empty folder allowed and folder name must be greater than fifteen characters')
        return redirect(url_for('home'))
    else:
        try:
            os.mkdir(os.path.join(usercontentfolders , newFolderName))
            if newFolderName not in allFolders:
                allFolders.append(newFolderName)
        except  FileExistsError:
            print("This Folder Already exists")
        except Exception:
            print("An error occured")
    return redirect(url_for('home'))

@app.route("/open-folder/<foldername>")
def openSpecificFolder(foldername):
    return render_template('media.html')


@app.route("/open-folder")
def openFolder():
    recievedFolderName = request.args.get('name' , None)
    if not len(recievedFolderName.strip()) == 0 and not recievedFolderName == None:
        print(url_for('openSpecificFolder' , foldername=recievedFolderName))
        return url_for('openSpecificFolder' , foldername=recievedFolderName)
    else:
        print('Error Cannot open Folder')
    
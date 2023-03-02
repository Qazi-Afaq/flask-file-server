from flask import Flask  , render_template , request , url_for , redirect
import os


usercontentfolders = os.path.join(os.getcwd() , 'static' , 'usercontentfolders')
# allFolders = os.listdir(usercontentfolders)
allFolders = [f for f in os.listdir(usercontentfolders) if not os.path.isfile(os.path.join(usercontentfolders , f))]
allowedMediaFilesList = ['mp4' , 'png' , 'jpg' , 'jpeg']


app = Flask(__name__)

@app.route("/")
def home():
    # allFolders = os.listdir(usercontentfolders)
    allFolders = [f for f in os.listdir(usercontentfolders) if not os.path.isfile(os.path.join(usercontentfolders , f))]
    return render_template('home.html' , allFolders=allFolders , urlForOpeningFolders=url_for('openFolder'))

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

@app.route("/openspecificfolder/<foldername>")
def openSpecificFolder(foldername):

    try:
        pageNo = abs(int(request.args.get('pg' , 1)))
    except Exception:
        pageNo = 1

    currentFolderMediaPath = os.path.join(os.getcwd() , 'static' , 'usercontentfolders' , foldername)
    start = 20 * (pageNo-1)
    end = start + 20

    currentFolderMedia = [f for f in os.listdir(currentFolderMediaPath)[start:stop] if os.path.isfile(os.path.join(currentFolderMediaPath , f)) and f.split('.')[-1].lower() in allowedMediaFilesList]
    print(currentFolderMedia)

    kwargsToSend = {
        "folderName":foldername,
        "media":currentFolderMedia
    }
    return render_template('media.html' , **kwargsToSend)


@app.route("/open-folder")
def openFolder():
    recievedFolderName = request.args.get('name' , None)
    if not len(recievedFolderName.strip()) == 0 and not recievedFolderName == None and recievedFolderName in allFolders:
        return url_for('openSpecificFolder' , foldername=recievedFolderName)
    else:
        print('Error Cannot open Folder')
        return redirect(url_for('home'))

@app.route("/home_js")
def home_js():
    return render_template("/js/home.js")
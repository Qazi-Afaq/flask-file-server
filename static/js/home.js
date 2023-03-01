let plustBtn = document.querySelector('.make-folder-btn-div img');
let createFolderFormDiv = document.querySelector('.create-folder-form-div');
let cancelMakeFolderBtn = document.querySelector('.cancel-make-folder-btn');
let submitMakeFolderBtn = document.querySelector('.submit-make-folder-btn');
plustBtn.addEventListener('click' , function(e) {

    createFolderFormDiv.style.visibility = "visible";
    createFolderFormDiv.style.opacity = "100%";
    document.querySelector('main').style.display = "none";

})
cancelMakeFolderBtn.addEventListener('click' , function(e) {
    createFolderFormDiv.style.visibility = "hidden";
    createFolderFormDiv.style.opacity = "0%";
    document.querySelector('main').style.display = "block";
})
submitMakeFolderBtn.addEventListener('click' , function(e) {
    if (document.querySelector('.create-folder-form-div form input').value != "") {
        createFolderFormDiv.style.visibility = "hidden";
        createFolderFormDiv.style.opacity = "0%";
        document.querySelector('main').style.display = "block";
    }

})

// ajax requst on clicking folders

popupFunc_photo = function () {
    window.open('modify-photo', '', 'left=200, top=100, width=400, height=200')
    window.close()
}

callback_photo = function (avatar) {
    if(true){
        var ele = document.getElementById("myImg")
        ele.src="/media/profile_image/" + avatar
    }
}
popupFunc_firstname = function () {
    window.open('modify-firstname', '', 'left=200, top=100, width=400, height=200')
    window.close()
}
callback_firstname = function (firstname) {
    var ele = document.getElementById("firstname_id")
    ele.innerHTML = firstname
}
popupFunc_lastname = function () {
    window.open('modify-lastname', '', 'left=200, top=100, width=400, height=200')
    window.close()
}
callback_lastname = function (lastname) {
    var ele = document.getElementById("lastname_id")
    ele.innerHTML = lastname
}
popupFunc_username = function () {
    window.open('modify-username', '', 'left=200, top=100, width=400, height=200')
    window.close()
}
callback_username = function (username) {
    var ele = document.getElementById("username_id")
    ele.innerHTML = username
}
popupFunc_confirmEmail = function () {
    window.open('confirm-email', '', 'left=200, top=100, width=400, height=200')
    window.close()
}
popupFunc_password = function () {
    window.open('modify-password', '', 'left=200, top=100, width=400, height=200')
    window.close()
}
callback_password = function () {
}
popupFunc_age = function () {
    window.open('modify-age', '', 'left=200, top=100, width=400, height=200')
    window.close()
}
callback_age = function (age) {
    var ele = document.getElementById("age_id")
    ele.innerHTML = age
}
popupFunc_bio = function () {
    window.open('modify-bio', '', 'left=200, top=100, width=400, height=200')
    window.close()
}
callback_bio = function (bio) {
    var ele = document.getElementById("bio_id")
    ele.innerHTML = bio
}
$('#student_button').click(function () {
    var pass1 = document.getElementById('password1').value;
    var pass2 = document.getElementById('password2').value;

    if ((pass1.length < 6) || (pass1.length > 20)) {

        document.getElementById('msg1').innerHTML = 'password must be 6+ character';
        return false;
    }

    if (pass1 != pass2) {
        document.getElementById('msg1').innerHTML = 'password did not match';
        return false

    }

    if (pass1.match(/[A-Z]/) && pass1.match(/[a-z]/) && pass1.match(/[0-9]/)) {
        return true
    }
    else {
        document.getElementById('msg1').innerHTML = 'password must be 1 lowercase 1 uppercase and 1 number';
        return false
    }


});
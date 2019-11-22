let firstname = document.getElementById("firstname");
let lastname = document.getElementById("lastname");
let password = document.getElementById("password");
let date = document.getElementById("date");
let email = document.getElementById("email");
let favoriteteam = document.getElementById("favoriteteam");


function createUser() {
    if(checkRegistrationField()) {
        ws.send("{\n" +
            "    \"request\": {\n" +
            "        \"first_name\": \"" + firstname.value + "\",\n" +
            "        \"last_name\": \"" + lastname.value + "\",\n" +
            "        \"date_of_birth\": \"" + date.value + "\",\n" +
            "        \"email\": \"" + email.value + "\",\n" +
            "        \"password\": \"" + password.value + "\",\n" +
            "        \"favourite_team\": \"" + favoriteteam.value + "\"\n" +
            "    },\n" +
            "    \"request_type\": \"user_registration\"\n" +
            "}");
    }
    console.log("Send registration request")
}

function loginUser() {
    if (checkLoginFields()) {
        ws.send("{\n" +
            "    \"request\": {\n" +
            "        \"email\": \"" + email.value + "\",\n" +
            "        \"password\": \"" + password.value + "\"\n" +
            "    },\n" +
            "    \"request_type\": \"user_login\"\n" +
            "}");
    }
    console.log("Send login request")
}

function userUpdate() {
    ws.send("{\n" +
        "    \"request\": {?},\n" +
        "    \"request_type\": \"user_update\"\n" +
        "}");
}

function checkRegistrationField() {
    return email.checkValidity() &&
        password.checkValidity() &&
        firstname.checkValidity() &&
        lastname.checkValidity() &&
        date.checkValidity() &&
        favoriteteam.checkValidity()
}

function checkLoginFields() {
    return email.checkValidity() &&
        password.checkValidity()
}
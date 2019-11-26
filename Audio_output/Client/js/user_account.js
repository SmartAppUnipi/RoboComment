let email           = document.getElementById("email");
let password        = document.getElementById("password");
let firstname       = document.getElementById("firstname");
let lastname        = document.getElementById("lastname");
let r_password      = document.getElementById("password");
let date            = document.getElementById("date");
let r_email         = document.getElementById("email");
let favoriteteam    = document.getElementById("favoriteteam");
const  DEBUG        = false;

function createUser() {


    if (!DEBUG){
        if((check(r_email) && check(r_password) && check(firstname)
            && check(lastname) && check(date) && check(favoriteteam))) {

            showSnack();

            ws.send("{\n" +
                "    \"request\": {\n" +
                "       \"user\": {\n" +
                "           \"first_name\": \"" + firstname.value + "\",\n" +
                "           \"last_name\": \"" + lastname.value + "\",\n" +
                "           \"date_of_birth\": \"" + date.value + "\",\n" +
                "           \"email\": \"" + email.value + "\",\n" +
                "           \"password\": \"" + password.value + "\",\n" +
                "           \"favourite_team\": \"" + favoriteteam.value + "\"\n" +
                "       }\n" +
                "    },\n" +
                "    \"request_type\": \"user_registration\"\n" +
                "}");
            console.log("Send registration request")
        }
    }else{
        showSnack();

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
        console.log("Send registration request")
    }

}

function loginUser() {


    if (check(email) && check(password)){
        ws.send("{\n" +
            "    \"request\": {\n" +
            "       \"user\": {\n" +
            "           \"email\": \"" + email.value + "\",\n" +
            "           \"password\": \"" + password.value + "\"\n" +
            "       }\n" +
            "    },\n" +
            "    \"request_type\": \"user_login\"\n" +
            "}");

        console.log("Send login request")
    }
}

function userUpdate() {
    ws.send("{\n" +
        "    \"request\": {?},\n" +
        "    \"request_type\": \"user_update\"\n" +
        "}");
}

function check(input) {
    if (input.value === null || input.value === "") {
        input.setCustomValidity("Please fill the filed");
        input.reportValidity();

        return false;
    } else {
        // input is fine -- reset the error message
        input.setCustomValidity('');
        input.reportValidity();
        return  true;

    }
}
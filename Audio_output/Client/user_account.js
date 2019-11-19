const KBIP = "ip";

let name = document.getElementById("name");
let surname = document.getElementById("surname");
let password = document.getElementById("password");
let date_of_birth = document.getElementById("date");
let email = document.getElementById("email");
let favourite_team = document.getElementById("team");

function createUser() {
    if(checkRegistrationField()) {
        let KBhttp = new XMLHttpRequest();
        // KBhttp.open("POST", KBIP + "/users", true);
        // KBhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
        KBhttp.send("{\n" +
            "    \"users\": {\n" +
            "        \"first_name\": \"" + name.textContent + "\",\n" +
            "        \"last_name\": \"" + surname.textContent + "\",\n" +
            "        \"date_of_birth\": \"" + date_of_birth.textContent + "\",\n" +
            "        \"email\": \"" + email.textContent + "\",\n" +
            "        \"password\": \"" + password.textContent + "\",\n" +
            "        \"favourite_team\": \"" + favourite_team.textContent + "\"\n" +
            "    }\n" +
            "    \"request_type\": \"create\"\n" +
            "}");

        KBhttp.addEventListener("load", function () {
            if (KBhttp.readyState === 4) {
                if (KBhttp.status === 200) {
                    console.log("user created");
                } else if (KBhttp.status === 400) {
                    alert("This user already exists!")
                }
            }
        })
    }
}

function loginUser() {
    if (checkLoginFields()) {
        let KBhttp = new XMLHttpRequest();

        KBhttp.open("GET", KBIP + "/users/login", true);
        KBhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
        KBhttp.send("{\n" +
            "    \"login\": {\n" +
            "        \"email\": \"" + email + "\",\n" +
            "        \"password\": \"" + password + "\"\n" +
            "    }\n" +
            "    \"request_type\": \"login\"\n" +
            "}");

        KBhttp.addEventListener("load", function () {
            if (KBhttp.readyState === 4) {
                if (KBhttp.status === 200) {
                    console.log("Login ok");
                } else if (KBhttp.status === 400) {
                    alert("This user already exists!")
                }
            }
        })
    }
}

function checkRegistrationField() {
    let alertText="";
    if (name.textContent === null) {
        alertText = alertText+"Name\n"
    }
    if (surname.textContent === null) {
        alertText = alertText+"Surname\n";
    }
    if (favourite_team.textContent === null) {
        alertText = alertText+"Favourite team is missing\n";
        return false
    }
    if (date_of_birth.textContent === null) {
        alertText = alertText+"Date of birth\n";
    }
    if (password.textContent === null) {
        alertText = alertText+"Password\n";
    }
    if (email.textContent === null) {
        alertText = alertText+"Email\n";
    }

    if (alertText === "") {
        alert("Theese fields are missing:\n"+alertText);
        return false
    }
    else
        return true
}

function checkLoginFields() {
    let alertText="";
    if (password.text === null) {
        alertText = alertText+"Password\n";
    }
    if (email.text === null) {
        alertText = alertText+"Email\n";
    }

    if (alertText === "") {
        alert("Theese fields are missing:\n"+alertText);
        return false
    }
    else
        return true
}
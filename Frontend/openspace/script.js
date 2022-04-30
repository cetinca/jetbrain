console.log("app started")
const buttons = document.querySelectorAll("input");

window.onload = function () {
    buttons.forEach(function (button) {
        if (button.id != "ok" && button.id != "pass") {
            button.disabled = true;
        }
    })
};

function passCheck() {
    const pwd = document.getElementById("pass")
    if (pwd.value === "TrustNo1") {
        enable()
        console.log("Password accepted!")
    } else {
        console.log("Wrong password!")
    }
}

enable = function () {
    buttons.forEach(function (button) {
        if (button.id != "ok" && button.id != "pass" && button.id != "launch") {
            button.disabled = false;
        } else {
            button.disabled = true
        }
    })
};

function checkRocket () {
    console.log("Launch in progress!")
    let checks = document.querySelectorAll(".check-buttons input")
    let checksOK = true
    checks.forEach(function (check){
        if (check.checked == false) {
            checksOK = false
        }
    })
    checks = document.querySelectorAll(".levers input")
    checks.forEach(function (check){
        if (check.value != 100) {
            checksOK = false
        }
    })
    if (checksOK) {
        let element = document.getElementById("launch");
        element.disabled = false;
    }
}

function fire () {
    let element = document.getElementById("r-07")
    element.classList.add("flying");
    console.log("Rocket is flying!");
    element = document.getElementById("launch");
    element.disabled = true;
}
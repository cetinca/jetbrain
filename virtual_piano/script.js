/**
document.addEventListener("keydown", function (event) {
    console.log(event.code);
    console.log(event.key);
    if (event.key == "W") {
        console.log("w Pressed");
    }
});
*/

const piano = ["a", "d", "f", "g", "h", "j", "s", "e", "t", "u", "w", "y"];
// const piano = "asdfghj";

document.addEventListener("keydown", async function (event) {
    const isKey = piano.includes(event.key.toLowerCase());
    const element = document.getElementById(event.key.toLowerCase())
    if (isKey) {
        console.log(`The '${event.key}' is pressed.`);
        findSound(event.key.toLowerCase()).play()
    } else {
        console.log("This is not a piano key!")
    }
    element.style.transform = "scale(0.98)";
    await sleep(100);
    element.style.transform = "scale(1)";
});

function findSound(key) {
    switch (key) {
        case "a":
            return (new Audio("./white_keys/A.mp3"));
        case "d":
            return (new Audio("./white_keys/D.mp3"));
        case "f":
            return (new Audio("./white_keys/F.mp3"));
        case "g":
            return (new Audio("./white_keys/G.mp3"));
        case "h":
            return (new Audio("./white_keys/H.mp3"));
        case "j":
            return (new Audio("./white_keys/J.mp3"));
        case "s":
            return (new Audio("./white_keys/S.mp3"));
        case "e":
            return (new Audio("./black_keys/E.mp3"));
        case "t":
            return (new Audio("./black_keys/T.mp3"));
        case "u":
            return (new Audio("./black_keys/U.mp3"));
        case "w":
            return (new Audio("./black_keys/W.mp3"));
        case "y":
            return (new Audio("./black_keys/Y.mp3"));
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
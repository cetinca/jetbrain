document.getElementById("upper-case").addEventListener("click", function () {
    let element = document.getElementById("text-area");
    element.value = element.value.toUpperCase();
})

document.getElementById("lower-case").addEventListener("click", function () {
    let element = document.getElementById("text-area");
    element.value = element.value.toLowerCase();
})

document.getElementById("proper-case").addEventListener("click", function () {
    let element = document.getElementById("text-area");
    element.value = letterToUpper(element.value);
})

document.getElementById("sentence-case").addEventListener("click", function () {
    let element = document.getElementById("text-area");
    element.value = sentenceToUpper(element.value);
})

document.getElementById("save-text-file").addEventListener("click", function () {
    let element = document.getElementById("text-area");
    download("text.txt", element.value)
})

let newString
function letterToUpper(text) {
    newString = ""
    let itemList = text.toLowerCase().split(" ");
    itemList.forEach(function(item){
        item = item[0].toUpperCase() + item.slice(1);
        newString += item + " "
    })
    console.log(newString.slice(0,-1))
    return newString.slice(0,-1)
}

function sentenceToUpper(text) {
    newString = ""
    let itemList = text.toLowerCase().split(". ");
    itemList.forEach(function(item){
        item = item[0].toUpperCase() + item.slice(1);
        newString += item + ". "
    })
    console.log(newString.slice(0,-2))
    return newString.slice(0,-2)
}

function download(filename, text) {
    let element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

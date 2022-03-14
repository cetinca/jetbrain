window.onload = function () {
    console.log("page is loading!!!")
    let data = getItems()
    console.log(data)
   data.forEach(function(element, index, array){
       createItem(element.inputText, element.ID, element.estatus) })
};

function addItem() {
    let inputText = document.getElementById("input-task").value;
    let ID = getID();
    let estatus = false;
    createItem(inputText, ID, estatus);
    let todo = {
        "inputText": inputText,
        "ID": ID,
        "estatus": estatus
    }
    let data = getItems()
    data.push(todo)
    storeItems(data)
}

function createItem(inputText, ID, estatus) {
    let li = document.createElement("li");
    li.id = ID
    let checkbox = document.createElement("input")
    checkbox.type = 'checkbox';
    checkbox.checked = estatus;
    checkbox.onclick = function () {
        lineThrough(this)
    };
    li.appendChild(checkbox);

    // if (estatus) {lineThrough(checkbox)}  //to add class for line through

    let span = document.createElement("span");
    if (estatus) {span.className = "task completed";} else {span.className = "task";}

    let p = document.createElement("p");
    let text = document.createTextNode(inputText);
    li.appendChild(span).appendChild(p).appendChild(text);

    let button = document.createElement("button");
    // button.addEventListener("click", removeItem)
    button.onclick = function () {
        removeItem(this)
    };
    button.className = "delete-btn";
    // button.id = ID;
    let img = document.createElement("img");
    img.src = "delete.png";
    img.width = 16;
    img.height = 20;
    li.appendChild(button).appendChild(img)

    document.getElementById("task-list").appendChild(li);
    document.getElementById("input-task").value = null
}

function removeItem(element) {
    let li = element.parentElement
    console.log(`${li.id} has been deleted!`)
    deleteFromStore(li.id)
    li.remove()
}

function getID() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

function lineThrough(element) {
    let parent = element.parentElement
    let task = parent.querySelector("span")
    if (element.checked) {
        task.classList.add("completed")
    } else {
        task.classList.remove("completed")
    }
    let data = getItems()
    data.forEach(function(todo, index, array){
        if (todo.ID === parent.id){
            todo.estatus = element.checked
        }
         })
    storeItems(data)
}

function lineThroughAlternative() {
    let elements = document.getElementsByTagName("li")
    for (let element of elements) {
        let checkBox = element.querySelector("input")
        let task = element.querySelector("span")
        if (checkBox.checked) {
            task.classList.add("completed")
        } else {
            task.classList.remove("completed")
        }
    }
}

function storeItems(data) {
    localStorage.setItem("todos", JSON.stringify(data))
}

function getItems() {
    let data = JSON.parse(localStorage.getItem("todos"))
    if (!data){
        return []
    } else {
        return data
    }
}

function deleteFromStore(ID) {
    let data = getItems()
    for (let i = data.length-1; i>=0; i--) {
        if (data[i].ID === ID) {
            data.splice(i, 1)
        }
    }
    storeItems(data)
}

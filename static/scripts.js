
// ADD TODO ITEM

function addTodo() {

    let todo = document.forms["todoForm"]["todo"].value;
    console.log("addTodo function called."); // Check if the function is called
    // Check if the todo is not empty
    if (!todo) {
    alert("Please enter a to-do item.");
    return false;
    }

    params = 'todo='+todo;

    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", '/AddTodo', true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function(){
        if (xhttp.readyState === 4 && xhttp.status === 200) {
        console.log(xhttp.responseText);
        // New TODO <li contenteditable="true" class="todoItem">{{todo}}</li>
        let todoItem = document.createElement("li");
        todoItem.contentEditable = true;
        todoItem.classList.add("todoItem");
        todoItem.innerHTML = todo;
        // CHECKBOX <input type="checkbox" class="complete" value="complete" onclick="completeTodo()">
        let myCheckbox = document.createElement("input");
        myCheckbox.type = "checkbox";
        myCheckbox.classList.add("complete") ;
        myCheckbox.onclick = "completeTodo()";
        // Add new todo and Chkbx into listItem div into todoList div 
        let todoList = document.getElementById("todoList");
        let listItem = document.createElement("div");
        todoList.appendChild(listItem);

        listItem.classList.add("listItem");
        listItem.appendChild(todoItem);
        listItem.appendChild(myCheckbox);
      

        } else {
        console.error(xhttp.statusText);
        }
    };
    xhttp.send(params);
    return false;
    };


// UPDATE Todo
function updateTodo() {
    // Get all the Todos
    const todoList = document.getElementById("todoList");
    const todos = todoList.querySelectorAll("li.todoItem");        
    // Get the content in  a list
    const todoItems = [];
    for (const item of todos){
        todoItems.push(item.textContent);
    }
    // JSON
    const jsonTodos = JSON.stringify(todoItems);
    console.log(jsonTodos);

    // Check if the todo is not empty
    if (!todos) {
        alert("Please enter a to-do item.");
        return false;
    }
    // Create request
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", '/UpdateTodo', true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.onreadystatechange = function(){
        if (xhttp.readyState === 4 && xhttp.status === 200) {
        console.log(xhttp.responseText);
        //  Display success message in page
        let msg = "todos saved successfully";
        let msgP = document.getElementById("msg");
        msgP.innerHTML = msg;

        } else {
        console.error(xhttp.statusText);
        }
    };
    // Send request
    xhttp.send(jsonTodos);
    return false;
    };


// COMPLETE todo
function completeTodo() {
    let completeCheck = document.querySelectorAll('input[class="complete"]:checked');
    completeCheck = completeCheck[0];
    parent = completeCheck.parentElement;
    todo = parent.querySelector(".todoItem").textContent;
    console.log(todo);
    parent.remove();

    // completeItem = completeCheck.previousSibling;
    // previousSib = completeItem.previousSibling;
    // prepresib = previousSib.previousSibling;
    // console.log(completeCheck);
    // console.log(completeItem);
    // console.log(previousSib);
    // console.log(prepresib);
    // // let completeCheck = document.querySelectorAll('input[class="complete"]:checked');
    // let allCheck = document.getElementsByClassName("complete");
    // let checked = allCheck.checked;
    // console.log(allCheck);
    // console.log(checked);

    // let parent = checked.parentElement;
    // console.log(parent);
}

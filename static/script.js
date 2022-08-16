

//selector
const transactionInput = document.querySelector(".transaction-input");
const transactionMethod = document.querySelector(".transaction-input-method");
const transactionType = document.querySelector(".transaction-input-type");
const transactionAmout = document.querySelector(".transaction-input-amount");
const transactionButton = document.querySelector(".transaction-button");
const transactionList = document.querySelector(".transaction-list");

//event listeners
transactionButton.addEventListener('click', addTransaction);

//Functions

function addTransaction(e) {
    //prevent form from submiting
    e.preventDefault();
    
    //transaction DIV
    const transactionDiv = document.createElement("div");
    transactionDiv.classList.add("transaction");
    //create list
    const newTransaction = document.createElement("li");
    newTransaction.innerText = transactionInput.value;
    newTransaction.classList.add("transaction-item");
    transactionDiv.appendChild(newTransaction);
    

    //delete button
    const deleteButton = document.createElement("button");
    deleteButton.innerHTML = '<i class="fa-solid fa-square-minus"></i>';
    deleteButton.classList.add("delete-btn");
    transactionDiv.appendChild(deleteButton);

    //apend to list

    transactionList.appendChild(transactionDiv);
}
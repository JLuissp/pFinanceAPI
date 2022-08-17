

//selector
const transactionInput = document.querySelector(".transaction-input");
const transactionMethod = document.querySelectorAll("input[name=payment-method]");
const transactionType = document.querySelectorAll("input[name=transaction-type]");
const transactionAmout = document.querySelector(".transaction-input-amount");
const transactionButton = document.querySelector(".transaction-button");
const transactionList = document.querySelector(".transaction-list");
const commitButton = document.querySelector(".submit-to-db-btn");
var jsonItems = [];

//event listeners
transactionButton.addEventListener('click', addTransaction);
transactionList.addEventListener('click',deleteSingleItem)

//Functions


function deleteSingleItem(e){
    const item = e.target;
    //delete transaction
    if(item.classList[0]=='delete-btn'){
        item.parentElement.remove();
        console.log(transactionList);
    }
}

function addTransaction(e) {    
    //prevent form from submiting
    e.preventDefault();
    //transaction DIV
    const transactionDiv = document.createElement("div");
    transactionDiv.classList.add("transaction");
    //create list
    if (transactionMethod[0].checked){
        const newTransaction = document.createElement("dl");
        newTransaction.innerHTML = '<i class="fa-regular fa-money-bill-1">&nbsp;&nbsp;'+transactionInput.value+'</i>';
        const newTransactionDescription = document.createElement("dd")
        if(transactionType[0].checked){
            newTransactionDescription.innerText = transactionAmout.value;

            var concepto = transactionInput.value;
            var payment_method = transactionMethod[0].value;
            var transaction_type=transactionType[0].value;
            var transaction_amount=transactionAmout.value;
            var dictItems = '{"date": "null", "concept":"'+concepto+'", "pay_method":'+payment_method+', "transaction_type":'+transaction_type+', "amount":'+transaction_amount+'}-';

            jsonItems.push(dictItems);
        }
        else if (transactionType[1].checked){
            newTransactionDescription.innerText = '-'+transactionAmout.value;
            var concepto = transactionInput.value;
            var payment_method = transactionMethod[0].value;
            var transaction_type=transactionType[1].value;
            var transaction_amount='-'+transactionAmout.value;
            var dictItems = '{"date": "null", "concept":"'+concepto+'", "pay_method":'+payment_method+', "transaction_type":'+transaction_type+', "amount":'+transaction_amount+'}-';

            jsonItems.push(dictItems);
        }
        newTransaction.classList.add("transaction-item");
        newTransaction.appendChild(newTransactionDescription);
        transactionDiv.appendChild(newTransaction);
    }
    else if(transactionMethod[1].checked){
        const newTransaction = document.createElement("li");
        newTransaction.innerHTML = '<i class="fa-regular fa-credit-card">&nbsp;&nbsp;'+transactionInput.value+'</i>';
        newTransaction.classList.add("transaction-item");
        const newTransactionDescription = document.createElement("dd")
        if(transactionType[0].checked){
            newTransactionDescription.innerText = transactionAmout.value

            var concepto = transactionInput.value;
            var payment_method = transactionMethod[1].value;
            var transaction_type=transactionType[0].value;
            var transaction_amount=transactionAmout.value;
            var dictItems = '{"date": "null", "concept":"'+concepto+'", "pay_method":'+payment_method+', "transaction_type":'+transaction_type+', "amount":'+transaction_amount+'}-';

            jsonItems.push(dictItems);;
        }
        else if (transactionType[1].checked){
            newTransactionDescription.innerText = '-'+transactionAmout.value

            var concepto = transactionInput.value;
            var payment_method = transactionMethod[1].value;
            var transaction_type=transactionType[1].value;
            var transaction_amount='-'+transactionAmout.value;
            var dictItems = '{"date": "null", "concept":"'+concepto+'", "pay_method":'+payment_method+', "transaction_type":'+transaction_type+', "amount":'+transaction_amount+'}-';

            jsonItems.push(dictItems);
        }

        newTransaction.classList.add("transaction-item");
        newTransaction.appendChild(newTransactionDescription);
        transactionDiv.appendChild(newTransaction);
    }
    //delete button
    const deleteButton = document.createElement("button");
    deleteButton.innerHTML = '<i class="fa-solid fa-square-minus"></i>';
    deleteButton.classList.add("delete-btn");
    transactionDiv.appendChild(deleteButton);

    //apend to list
    transactionList.appendChild(transactionDiv);

    //clear transaction input
    transactionInput.value = ""
    transactionAmout.value = ""
}
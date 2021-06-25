

window.onload = () => {

    const addDeathButtons = document.getElementsByClassName('add-death-button');
    const removeDeathButtons = document.getElementsByClassName('remove-death-button');
    const bossNameFields = document.getElementsByClassName('boss-name');
    const removeEntryButtons = document.getElementsByClassName('remove-entry-button');
    const isCompletedChecks = document.getElementsByClassName('is-completed');

    Array.from(addDeathButtons).forEach(button => button.addEventListener('click', onDeathButtonClicked(1, button)));
    Array.from(removeDeathButtons).forEach(button => button.addEventListener('click', onDeathButtonClicked(-1, button)));
    Array.from(bossNameFields).forEach(element => element.addEventListener('change', function() {modifyBossName(element);}));
    Array.from(removeEntryButtons).forEach(button => button.addEventListener('click', function() {removeEntry(button);}));
    Array.from(isCompletedChecks).forEach(checkbox => checkbox.addEventListener('click', function() {sendCompletedChangedRequest(checkbox);}));
}

function sendCompletedChangedRequest(checkbox) {
    const rowId = parseInt(checkbox.id.match(/\d+/g)[0]);

    console.log("Sending completed request");

    let state = {
        iscompleted: checkbox.checked,
        rowId: rowId
    }

    let request = new XMLHttpRequest();
    request.open('POST', "/", true);
    request.setRequestHeader('Content-Type', 'application/json');

    request.addEventListener('load', function(){
        if(request.status >= 200 && request.status < 400){
            let response = JSON.parse(request.responseText);
            if(!response.success){
                checkbox.checked = !state.iscompleted;
            }
        }else{
            alert("Error in network request: " + request.statusText);
        }
    });

    request.send(JSON.stringify(state));
}

function onDeathButtonClicked(amount, button){
    return function(){
        modifyDeath(amount, button);
    }
}

function removeEntry(button){
    let request = new XMLHttpRequest();
    request.open('POST', "/", true);
    request.setRequestHeader('Content-Type', 'application/json');

    const rowId = parseInt(button.id.match(/\d+/g)[0]);

    let state = {
        remove: true,
        rowId: rowId
    };

    request.addEventListener('load', function(){
        if(request.status >= 200 && request.status < 400){
            let response = JSON.parse(request.responseText);
            if(response.success){
                document.getElementById('boss-table').deleteRow(document.getElementById(`boss-row-${rowId}`).rowIndex);
            }
        }else{

            alert("Error in network request: " + request.statusText);
        }
    });

    request.send(JSON.stringify(state));
}

function modifyDeath(amount, button) {

    let request = new XMLHttpRequest();
    request.open('POST', "/", true);
    request.setRequestHeader('Content-Type', 'application/json');

    const rowId = parseInt(button.id.match(/\d+/g)[0]);

    let state = {
        deathChange: amount,
        rowId: rowId
    };

    request.addEventListener('load', function(){
        if(request.status >= 200 && request.status < 400){
            let response = JSON.parse(request.responseText);
            if(response.success){

                let currentDeathCountElement = document.getElementById(`death-count-${rowId}`);
                let currentDeathCount = parseInt(currentDeathCountElement.innerText) + amount;

                if(currentDeathCount < 0)
                    currentDeathCount = 0;

                const totalDeathCounter = document.getElementById('total-deaths-counter');

                let oldTotal = parseInt(totalDeathCounter.innerText.match(/\d+/g)[0]);

                let newTotal = oldTotal + amount;

                if(newTotal < 0)
                    newTotal = 0

                totalDeathCounter.innerText = "Total Deaths: " + (newTotal).toString();
                currentDeathCountElement.innerText = (currentDeathCount).toString();
            }
        }else{
            alert("Error in network request: " + request.statusText);
        }
    });

    request.send(JSON.stringify(state));
}


function modifyBossName(element){

    const rowId = parseInt(element.id.match(/\d+/g)[0]);

    let state = {
        newName: element.value,
        rowId: rowId
    };


    let request = new XMLHttpRequest();
    request.open('POST', "/", true);
    request.setRequestHeader('Content-Type', 'application/json');

    request.addEventListener('load', function(){
        if(request.status >= 200 && request.status < 400){
            let response = JSON.parse(request.responseText);
            if(!response.success){
                element.value = response.oldName;
            }
        }else{
            alert("Error in network request: " + request.statusText);
        }
    });

    request.send(JSON.stringify(state));
}

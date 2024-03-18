function checking_cookie(){
    // Get cookies
    const cookies = document.cookie.split(';');

    // Checking cookies
    for (const cookie of cookies) {
        const [key, value] = cookie.split('='); //Split cookie string
        // check if cookie is block_notification = true
        if(key === ' block_notification' && value === 'true'){
            document.getElementById('popupPushBox').remove();
        }
    }
}
checking_cookie()

function close_popupAppeal(e){
    e.parentElement.parentElement.parentElement.remove(); //Remove id #popupPushBox
}

function cloeAndBlock_popupAppeal(e){
    close_popupAppeal(e); //Remove id #popupPushBox

    //Request to server for adding sessions so that the notification does not show anymore
    const xhr = new XMLHttpRequest();
    //Request to server
    xhr.open("POST", "/block_notification");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function() {
        // If problem with server
        if(xhr.status !== 200){
            alert('Проблемы с сервером.')
        }
    };

    xhr.send(JSON.stringify(true));

}

function searchBook(e){
    document.getElementById('booksBoxText').style.display = 'none'; //Hide 'No resault' text
    document.getElementById('loading').style.display = 'block'; // Show loading animated span
    const book_name = document.getElementById('bookNameInp').value;
    // Search books by name
    const xhr = new XMLHttpRequest();
    //Request to server
    xhr.open("POST", "/search_book");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function() {
        // If problem with server
        if(xhr.status === 200){
            const response = JSON.parse(xhr.responseText); //Take all books data
            document.getElementById('loading').style.display = 'none'; // Hide loading animated span

            console.log(response)
            document.getElementById('resaultBox').innerHTML = response;
        }else{
            alert('Проблемы с сервером.')
        }
    };

    xhr.send(JSON.stringify(book_name));
}
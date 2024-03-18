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
    document.getElementById('resaultBox').innerHTML = ''; //Remove old finded books list
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

            if(response.length !== 0){ // Checking if responsed data is not empty
                // Create box
                let books_arr_box_html = '<div id="booksArrBox">';

                for (let i = 0 ; i < response.length; i++){
                    if (response[i]['title'].indexOf('писател') === -1){ // Writers are not added
                        // Add title
                        books_arr_box_html += `<h3>`+ response[i]['title'] +`</h3>`;
                        // If itle is book's sera, add books searching by seria

                        // Make books list
                        books_arr_box_html += '<ul>';
                        // Add book's button
                        for (let x = 0; x < response[i]['books'].length; x++){
                            //Make searching button
                            let button_html;
                            if (response[i]['title'].indexOf('серии') !== -1){ // Checking if dict is seria's dict
                                button_html = `<li><button class="booksSeriesButton" onclick="searchBookByDict('`+ response[i]['books'][x]['href'] +`')">`+ response[i]['books'][x]['book_title'] +`</button></li>`;
                            }else if(response[i]['title'].indexOf('книги') !== -1){ // Checking if dict is books
                                button_html = `<li><button class="booksButton" onclick="viewBook('`+ response[i]['books'][x]['href'] +`')">`+ response[i]['books'][x]['book_title'] +`</button></li>`;
                            }
                            // Add button to html variable
                            books_arr_box_html += button_html;
                        }
                        // Close ul
                        books_arr_box_html += '</ul>';
                    }
                }
                // Close main div
                books_arr_box_html += '</div>';
                document.getElementById('resaultBox').innerHTML = books_arr_box_html;
            }else{ // If responset dat is empty
                document.getElementById('booksBoxText').style.display = 'block'; //Show 'No resault' text
            }
        }else{
            alert('Проблемы с сервером.')
        }
    };

    xhr.send(JSON.stringify(book_name));
}

function searchBookByDict(_href){

}

function viewBook(_href){
    // View book's Description
}
let searchQueryInput = document.querySelector('#search-query')
let submitButton = document.querySelector('#submit-button')

submitButton.addEventListener('click', function() {

    let searchQuery = searchQueryInput.value 
    console.log(searchQuery)

})
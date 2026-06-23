const movieSearches = document.querySelectorAll('.searchBar input[type="text"]');
        
movieSearches.forEach((inputElement =>{
        inputElement.addEventListener('keydown', (event)=>{
            if (event.key == 'Enter') {
                event.preventDefault();
                triggerSearchMovie(inputElement);
            }
        })
    }))

function triggerSearchMovie(inputElement) {
    if (inputElement.id === "movieSearcherOne") {
        searchMovie('movieSearcherOne','resultsOne','movieOneTitle', 'movieOnePoster', 'selectedOne')
    } else if (inputElement.id === "movieSearcherTwo") {
        searchMovie('movieSearcherTwo','resultsTwo','movieTwoTitle', 'movieTwoPoster', 'selectedTwo')
    }
}

function searchMovie(inputID, divID, hiddenTitleID, hiddenPosterID, selectedDivID){
    const query = document.getElementById(inputID).value
    console.log("I want THIS movie:", query)

    const options = {
        method: 'GET',
        headers: {
            accept: 'application/json',
        }
    };

    fetch('/search?query=' + query, options)
        .then(res => res.json())
        .then(res => {
            let html = ""

            res.results.slice(0,5).forEach(element => {
                html += `<li onclick="selectMovie('${element.title}', '${element.poster_path}', '${element.release_date}', '${element.id}', '${divID}', '${hiddenTitleID}', '${hiddenPosterID}', '${selectedDivID}')">${element.title} (${element.release_date.slice(0,4)})</li>`
            }); 
            document.getElementById(divID).innerHTML = html;
            
        })
        .catch(err => console.error(err));
}

function selectMovie(title, poster, release, ID, divID, hiddenTitleID, hiddenPosterID, selectedDivID){
    console.log(selectedDivID)
    let year = release.slice(0,4);

    document.getElementById(selectedDivID).innerHTML = "<h2>" + title + " (" + year + ")" + "</h2>" +
            "<img src='https://image.tmdb.org/t/p/w500" + poster + "'>";

            document.getElementById(hiddenTitleID).value = title + " (" + year + ")";
            document.getElementById(hiddenPosterID).value = poster;

    document.getElementById(divID).innerHTML = ""
}
import {parse_people} from './people.js'

async function on_button_click() {
    const person = document.getElementById('character-id-input');

    let response = await fetch(`http://localhost:8000/api/v1/people/${person.value}`);
    const character_card = document.getElementById('character-card');

    if(response.ok == true){
        let data = await response.json();
        parse_people(data, character_card);
    }else{
        character_card.innerHTML = 'Error'
    }

};

const character_input = document.getElementById('character-form');

character_input.addEventListener('submit', function(event) {
    event.preventDefault();
    on_button_click();
});

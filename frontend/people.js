/**
 * @param {Object} personData - The user's name
 * @param {HTMLDivElement} canvas - The canvas to be overwritten
 * @returns null
 */
export function parse_people(personData, canvas){

canvas.innerHTML = `
  <div class="character-card">
    <h2>${personData.name}</h2>

    <div class="bio">
      <p><strong>Birth Year:</strong> ${personData.birth_year}</p>
      <p><strong>Gender:</strong> ${personData.gender}</p>
      <p><strong>Height:</strong> ${personData.height} cm</p>
      <p><strong>Mass:</strong> ${personData.mass} kg</p>
    </div>

    <div class="appearance">
      <h3>Appearance</h3>
      <ul>
        <li><strong>Hair:</strong> ${personData.hair_color}</li>
        <li><strong>Eyes:</strong> ${personData.eye_color}</li>
        <li><strong>Skin:</strong> ${personData.skin_color}</li>
      </ul>
    </div>

    <div class="links">
      <h3>Assets</h3>
      <p><strong>Films (${personData.films.length}):</strong></p>
      <ul>
        ${personData.films.map(film => `<li><a href="${film}" target="_blank">Film Link</a></li>`).join('')}
      </ul>

      <p><strong>Starships:</strong></p>
      <ul>
        ${personData.starships.length > 0
          ? personData.starships.map(ship => `<li><a href="${ship}" target="_blank">Ship Link</a></li>`).join('')
          : '<li>None</li>'}
      </ul>
    </div>
  </div>
`
};

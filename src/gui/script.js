const token_title_input = document.getElementById("token-title-input")
const token_add_button = document.getElementById("token-add-button")
const token_table_body = document.getElementById("token-table-body")

eel.expose
function displayToken(token)
{
    // Crear una nueva fila
    const row = document.createElement("tr");

    // Crear y agregar la celda del ID
    const idCell = document.createElement("td");
    idCell.textContent = token.id;
    row.appendChild(idCell);

    // Crear y agregar la celda del título
    const titleCell = document.createElement("td");
    titleCell.textContent = token.title;
    row.appendChild(titleCell);

    // Agregar la fila al cuerpo de la tabla
    token_table_body.appendChild(row);
}

function displayTokens(tokens)
{
    for (let token of tokens["tokens"])
    {
        displayToken(token)
    }
}

token_add_button.addEventListener("click", (event) => {
    let content = token_title_input.value;
    if (content != "")
    {
        eel.create_token(content) (displayToken);
        // this will get the token named from the title input field and
        // call the python script create_token to create the token and
        // store it in the json file
        // when we want to retrieve data from python using a js function
        // we need to pass a callback function from js file
        // in this case, the callback function is (displayToken) 
    }
})


eel.list_tokens() (displayTokens)
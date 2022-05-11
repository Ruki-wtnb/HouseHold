
fetch('http://localhost:8000/totals/list/2022-05', {
    mode: 'cors'
})
.then(response => response.json())
.then(res => {
    console.log(res);

    let table = document.getElementById("list-table")

    console.log(table.columns)

    for(let row of table.rows) {
        console.log(row.cells[1].id)
        console.log(row.cells[2].innerText)
    }

})

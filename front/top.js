
fetch('http://localhost:8000/totals/list/2022-05', {
    mode: 'cors'
})
.then(response => response.json())
.then(res => {
    let table = document.getElementById("list-table")

    console.log(Object.keys(res))
    for(let row of table.rows) {
        row.cells[2].innerText = res[row.cells[1].id]
    }

})

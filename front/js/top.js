

getTotal();

async function getTotal(){
    const res = await fetch('http://localhost:8000/totals/list/2022-05')
    .then(response => response.json());
    await insertValues(res)
    await createGraph(res)
}

async function insertValues(res){
    let table = document.getElementById("list-table")
    for(let row of table.rows) {
        row.cells[2].innerText = res[row.cells[1].id]
    }
}

async function createGraph(res){
    
    delete res.income
    delete res.spending
    delete res.balance
    
    const ctx = document.getElementById("myChart").getContext('2d');
    const myCHart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(res),
            datasets: [{
                data: Object.values(res)
            }]
        },
        options: {
            plugins: {
                colorschemes: {
                    scheme: 'brewer.Paired12'
                }
            }
        }
    });
}

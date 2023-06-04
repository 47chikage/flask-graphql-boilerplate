//medecins
function persons_list_disp(disp_id,instance){
  var table = document.getElementById(disp_id);
  var n_rows =table.rows.length;
  var row = table.insertRow(n_rows);
  var cell1= row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3=row.insertCell(2);
  cell1.innerHTML = instance.username;
  cell2.innerHTML = instance.role;
  link = create_link(instance.username);
  cell3.appendChild(link);
}

function create_link(username) {
  var link = document.createElement('a');
  link.href = `persons/${username}`;
  var button = document.createElement('button');
  button.textContent = 'See details';
  link.appendChild(button);
return link
}

function send_query(query,disp_id) {
  
  fetch('/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: query })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
      
    }
    return response.json();
  })
  .then(data => {
    if (data.error) {
      document.getElementById(disp_id).innerText = 'Error: ' + data.error;
    } else {
      data.result.persons.forEach(function(instance){

        persons_list_disp(disp_id,instance);
      });
    }
  })
  .catch(error => {
    console.log('Error:', error);
  });
}

function list_persons(disp_id){
  var query = 'query{persons{username role}}'

  try {
    send_query(query,disp_id);
    window.document.getElementById('list_button').disabled=true;
  } catch (error) {
    console.log('Error:', error);
  }
}

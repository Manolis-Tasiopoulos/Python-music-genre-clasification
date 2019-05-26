
let {PythonShell} = require('python-shell')
var path = require("path")


function Train() {

  var csv_path = document.getElementById("path").value

  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : [csv_path]
  }

  let pyshell = new PythonShell('training_model.py', options);
  var list = document.getElementById('list');

  pyshell.on('message', function(message) {
    if (message === "training")
    {

        pyshell.on('message', function(message)
        {
          var entry = document.createElement('li');
          entry.appendChild(document.createTextNode(message));
          list.appendChild(entry);
          if(message === "Model saved")
          {
            Swal.fire(
            'Finish training!',
            'click ok to continue',
            'success'
            )
          }
        })
    }


  })
  document.getElementById("path").value = "";
}


let {PythonShell} = require('python-shell')
var path = require("path")


function Analyse() {

  var db_path = document.getElementById("path").value

  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : [db_path]
  }

  let pyshell = new PythonShell('csv_creator.py', options);


  pyshell.on('message', function(message) {
    if (message === "analyse")
    {
      Swal.fire({
      title: 'Analyse your database',
      html: 'Progress: <strong></strong>',
      allowOutsideClick: false,
      onBeforeOpen: () => {
        Swal.showLoading()
        pyshell.on('message', function(message)
        {
          console.log(Swal.getContent().querySelector('strong').textContent = message)
          if (message === "finish")
          {
            Swal.fire(
            'Finish analysing!',
            'click ok to continue',
            'success'
            )

          }
        })


      },
      onClose: () => {
        pyshell.end(function (err,code,signal) {
          if (err) throw err;
          console.log('The exit code was: ' + code);
          console.log('The exit signal was: ' + signal);
          console.log('finished');
          console.log('finished');
        });
      }
      })
    }

  })
  document.getElementById("path").value = "";
}

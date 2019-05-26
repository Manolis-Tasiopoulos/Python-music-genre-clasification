
let {PythonShell} = require('python-shell')
var path = require("path")


function Predict() {

  var db_path = document.getElementById("path").value

  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : [db_path]
  }

  let pyshell = new PythonShell('predict_song.py', options);


  pyshell.on('message', function(message) {
    if (message === "predict")
    {
      Swal.fire({
      title: 'Analyse your database',
      html: 'Predict: <strong></strong>',
      allowOutsideClick: false,
      onBeforeOpen: () => {
        Swal.showLoading()
        Swal.getContent().querySelector('strong').textContent = db_path
        pyshell.on('message', function(message)
        {
          if (message === "results")
          {
            pyshell.on('message', function(message)
            {
              var entry = document.createElement('li');
              entry.appendChild(document.createTextNode(message));
              list.appendChild(entry);
              if(message === "---finish---")
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

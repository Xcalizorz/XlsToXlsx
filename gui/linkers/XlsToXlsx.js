function convert_to_xlsx() {

  document.getElementById("addFile").value = "Hang on..."
  var python = require("python-shell")
  var path = require("path")

    var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    pythonPath : '/usr/local/bin/python3'
  }

  var face = new python("__main__.py", options);

  face.end(function(err, code, message) {
    document.getElementById("addFile").value = "Adding the directory.";
    })

}

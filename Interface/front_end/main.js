const { app, BrowserWindow } = require('electron');
const path = require('path');
const { PythonShell } = require('python-shell');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });
  mainWindow.loadFile('index.html');
  setTimeout(() => {
    startPythonScript();
  }, 1500); // 3000 milliseconds (3 seconds) delay
}

function startPythonScript() {
  let pyshell = new PythonShell('Interface/game.py');

  pyshell.send(JSON.stringify([10]))

  pyshell.on('message', function(message) {
    console.log(message);
  })

  pyshell.end(function (err) {
    if (err){
      throw err;
    };
    console.log('finished');
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
var express = require('express');
var app = express();
const { spawn } = require('child_process');
const { readFile } = require('fs');
const { parse } = require('csv-parse');
var evento = new Object();
let eventos = [];
let eventos2 = [];
app.use(express.json());


//---------------------------------------------- LUNA -----------------------------------------------
readFile("TestMoon.csv", 'utf8', (err, fileContent) => {
    if (err) {
      console.error('Error reading file:', err);
      return;
    }
    parse(fileContent, { comment: '#', columns: true }, (parseError, rows) => {
      if (parseError) {
        console.error('Error parsing file:', parseError);
        return;
      }
      const directions = rows.map(row => row.filename);
      const dates = directions.map(direction => {
        const match = direction.match(/\d{4}-\d{2}-\d{2}/);
        return match ? match[0] : null;
      });
      
        const id = rows.map(row => row.evid);
        for (let i = 0; i < dates.length; i++) {
            let evento = {
              direction:  directions[i],
              id: id[i],
              date: dates[i]
            };
            eventos.push(evento);
        }
        console.log("----------------------LUNA----------------------");
        for (let i = 0; i < id.length; i++) {
            console.log(eventos[i]);
        }
        app.get('/moon', function(req, res) {
            console.log("LUNA");
            res.send(eventos);
        });
        app.post('/eventosLuna', function(req, res) {
            console.log(req.body);
            res.json(eventos[req.body.id]);
            const childPython = spawn('python', ['prueba.py', eventos[req.body.id].direction]);
            childPython.stdout.on('data', (data) => {
                console.log(`stdout: ${data}`);
            });
            childPython.stderr.on('data', (data) => {
                console.error(`stderr: ${data}`);
            });
            childPython.on('close', (code) => {
                console.log(`child process exited with code ${code}`);
            });

        });
    });
});

//---------------------------------------------- Marte -----------------------------------------------
readFile("TestMars.csv", 'utf8', (err, fileContent) => {
  if (err) {
    console.error('Error reading file:', err);
    return;
  }
  parse(fileContent, { comment: '#', columns: true }, (parseError, rows) => {
    if (parseError) {
      console.error('Error parsing file:', parseError);
      return;
    }
    const directions = rows.map(row => row.filename);
    const dates = directions.map(direction => {
      const match = direction.match(/\d{4}-\d{2}-\d{2}/);
      return match ? match[0] : null;
    });
    
      const id = rows.map(row => row.evid);
      for (let i = 0; i < dates.length; i++) {
          let evento = {
            direction:  directions[i],
            id: id[i],
            date: dates[i]
          };
          eventos2.push(evento);
      }
      console.log("----------------------LUNA----------------------");
      for (let i = 0; i < id.length; i++) {
          console.log(eventos2[i]);
      }
      app.get('/mars', function(req, res) {
          console.log("MARTE");
          res.send(eventos2); 
      });
      app.post('/eventosMarte', function(req, res) {
          console.log(req.body);
          res.json(eventos2[req.body.id]);
          const childPython = spawn('python', ['prueba.py', eventos2[req.body.id].direction]);
          childPython.stdout.on('data', (data) => {
              console.log(`stdout: ${data}`);
          });
          childPython.stderr.on('data', (data) => {
              console.error(`stderr: ${data}`);
          });
          childPython.on('close', (code) => {
              console.log(`child process exited with code ${code}`);
          });

      });
  });
});


app.listen(3000, () => {
    console.log('Server running on port 3000');
});
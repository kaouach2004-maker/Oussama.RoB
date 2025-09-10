// server/app.js
const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '..', 'frontend')));

const COMMANDS_FILE = path.join(__dirname, '..', 'commands.json');
const PENDING_DIR = path.join(__dirname, '..', 'pending_artifacts');

// Helpers
function ensureCommands(){
  if(!fs.existsSync(COMMANDS_FILE)){
    fs.writeFileSync(COMMANDS_FILE, JSON.stringify({pending:[], done:[]}, null, 2));
  }
}
ensureCommands();

// Routes
app.get('/api/status', (req, res) => {
  res.json({ok:true, status:"Oussama server running"});
});

app.get('/api/tasks', (req, res) => {
  ensureCommands();
  const data = JSON.parse(fs.readFileSync(COMMANDS_FILE));
  res.json(data);
});

app.post('/api/tasks', (req, res) => {
  ensureCommands();
  const { command } = req.body;
  if(!command) return res.status(400).json({ok:false, error:"missing command"});
  const data = JSON.parse(fs.readFileSync(COMMANDS_FILE));
  data.pending.push(command);
  fs.writeFileSync(COMMANDS_FILE, JSON.stringify(data, null, 2));
  return res.json({ok:true, added:command});
});

app.get('/api/pending_artifacts', (req, res) => {
  if(!fs.existsSync(PENDING_DIR)) return res.json([]);
  const files = fs.readdirSync(PENDING_DIR).filter(f=>f.endsWith('.json'));
  const out = files.map(f=>{
    try { return JSON.parse(fs.readFileSync(path.join(PENDING_DIR,f)))} catch(e){return null}
  }).filter(x=>x);
  res.json(out);
});

// Serve frontend
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html'));
});

// Start
const PORT = process.env.PORT || 3000;
app.listen(PORT, ()=> console.log(`Oussama server running on port ${PORT}`));

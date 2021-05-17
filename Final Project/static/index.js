const socket = io();
socket.on('connect', () => {
  
});

const impBtn = document.getElementById('impBtn');
const impVal = document.getElementById("imp");


const startBtn = document.getElementById('startBtn');
const engBtn = document.getElementById('engBtn');
const engVal = document.getElementById('eng');

  
setInterval(() => {
  socket.emit('ping-gps', 'dat')
}, 100)

socket.on('disconnect', () => {
  console.log('disconnect')
  });

impBtn.onclick = () => {
  socket.emit('impressions', ' ')
}

engBtn.onclick = () => {
  socket.emit('engagement', ' ')
}

startBtn.onclick = () => {
  console.log("start")
  socket.emit('start', '')
}

socket.on('impressions', (msg) =>{
  impVal.innerHTML = msg
});

socket.on('engagement', (msg) =>{
  engVal.innerHTML = msg
});

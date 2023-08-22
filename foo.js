const timeSlots = [
  "9:00 AM", "9:30 AM",
  "10:00 AM", "10:30 AM",
  "11:00 AM", "11:30 AM",
  "12:00 PM", "12:30 PM",
  "1:00 PM", "1:30 PM",
  "2:00 PM", "2:30 PM",
  "3:00 PM", "3:30 PM",
  "4:00 PM", "4:30 PM",
  "5:00 PM", "5:30 PM",
  "6:00 PM", "6:30 PM",
  "7:00 PM", "7:30 PM",
  "8:00 PM", "8:30 PM",
  "9:00 PM", "9:30 PM",
  "10:00 PM", "10:30 PM",
  "11:00 PM", "11:30 PM",
];
console.log("hello world");
const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"/* ... more days ... */];

const tableBody = document.getElementById("table-body");
let availDict = {};
const saveButton = document.getElementById("saveButton");

timeSlots.forEach(timeSlot => {
const row = document.createElement("tr");
const timeSlotCell = document.createElement("td");
timeSlotCell.textContent = timeSlot;
row.appendChild(timeSlotCell);

days.forEach(day => {
  const cell = document.createElement("td");
  cell.classList.add("availability-cell");
  const cellIdentifier = timeSlot + " " + day;
  saveButton.addEventListener("click", () => {
    if(cell.classList.contains("selected")){
      availDict[cellIdentifier] = 1;
    }
    else{
      availDict[cellIdentifier] = 0;
    }
    
  });
  availDict[cellIdentifier] = 0;
  row.appendChild(cell);
});

tableBody.appendChild(row);
});
const cells = document.querySelectorAll('.availability-cell');

let isMouseDown = false;

cells.forEach(cell => {
cell.addEventListener('mousedown', () => {
  isMouseDown = true;
  toggleAvailability(cell);
});

cell.addEventListener('mouseover', () => {
  if (isMouseDown) {
    toggleAvailability(cell);
  }
});
});

document.addEventListener('mouseup', () => {
  isMouseDown = false;
});

function toggleAvailability(cell) {
  cell.classList.toggle('selected');
}

const nameInput = document.getElementById("name");
let currentName = "";

nameInput.addEventListener("input", event => {
  currentName = event.target.value;
});

saveButton.addEventListener("click", event => {
  let pyInput = {"name": currentName, "availability": availDict}
  console.log(pyInput);
  const websocket = new WebSocket("ws://localhost:8001/");
  websocket.onopen = () =>websocket.send(JSON.stringify(pyInput));
});
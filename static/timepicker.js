// timepicker.js - Clock-style time picker for mobile
var tpSelectedHour = 0;
var tpSelectedMinute = 0;
var tpMode = 'hour';
var tpPeriod = (function() { var h = new Date().getHours(); return h >= 12 ? 'PM' : 'AM'; })();

function openTimePicker() {
  var overlay = document.getElementById('timePickerOverlay');
  overlay.classList.add('active');
  tpMode = 'hour';
  renderTimePickerClock();
  updateTpSelected();
}

function closeTimePicker() {
  document.getElementById('timePickerOverlay').classList.remove('active');
}

function selectAMPM(period) {
  tpPeriod = period;
  document.getElementById('tpAM').classList.toggle('active', period === 'AM');
  document.getElementById('tpPM').classList.toggle('active', period === 'PM');
  updateTpSelected();
}

function confirmTimePicker() {
  var h = tpSelectedHour;
  if (h === 0) h = 12;
  if (tpPeriod === 'PM' && h < 12) h += 12;
  if (tpPeriod === 'AM' && h === 12) h = 0;
  var m = tpSelectedMinute;
  var timeStr = (h < 10 ? '0' + h : h) + ':' + (m < 10 ? '0' + m : m);
  document.getElementById('birthTimeHidden').value = timeStr;
  var display = document.getElementById('timePickerDisplay');
  display.textContent = timeStr;
  display.classList.remove('time-display-placeholder');
  display.style.color = 'var(--text)';
  display.style.fontSize = '16px';
  display.style.fontWeight = '600';
  closeTimePicker();
}

function switchTimeMode(mode) {
  tpMode = mode;
  document.getElementById('tpHour').classList.toggle('active', mode === 'hour');
  document.getElementById('tpMinute').classList.toggle('active', mode === 'minute');
  renderTimePickerClock();
}

function renderTimePickerClock() {
  var clock = document.getElementById('tpClock');
  var hourHand = document.getElementById('tpHourHand');
  var minuteHand = document.getElementById('tpMinuteHand');

  clock.querySelectorAll('.time-picker-number').forEach(function(n) { n.remove(); });

  var size = 240, center = size / 2, radius = 90, numSize = 34, halfNum = numSize / 2;
  clock.style.width = size + 'px';
  clock.style.height = size + 'px';

  if (tpMode === 'hour') {
    hourHand.style.display = 'block';
    minuteHand.style.display = 'none';
    for (var i = 1; i <= 12; i++) {
      var angle = (i * 30 - 90) * Math.PI / 180;
      var x = center + radius * Math.cos(angle) - halfNum;
      var y = center + radius * Math.sin(angle) - halfNum;
      var num = document.createElement('div');
      num.className = 'time-picker-number' + (tpSelectedHour === (i % 12 === 0 ? 12 : i % 12) ? ' selected' : '');
      num.textContent = i;
      num.style.left = x + 'px';
      num.style.top = y + 'px';
      num.style.width = numSize + 'px';
      num.style.height = numSize + 'px';
      num.style.lineHeight = numSize + 'px';
      num.setAttribute('data-hour', i % 12);
      num.onclick = (function(h) {
        return function() {
          tpSelectedHour = h;
          tpMode = 'minute';
          document.getElementById('tpHour').classList.remove('active');
          document.getElementById('tpMinute').classList.add('active');
          renderTimePickerClock();
          updateTpSelected();
        };
      })(i % 12 === 0 ? 12 : i % 12);
      clock.appendChild(num);
    }
    var ha = (tpSelectedHour % 12) * 30;
    hourHand.style.transform = 'rotate(' + ha + 'deg)';
    hourHand.style.height = (radius - 10) + 'px';
  } else {
    hourHand.style.display = 'none';
    minuteHand.style.display = 'block';
    var mvals = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55];
    for (var i = 0; i < 12; i++) {
      var angle = (i * 30 - 90) * Math.PI / 180;
      var x = center + radius * Math.cos(angle) - halfNum;
      var y = center + radius * Math.sin(angle) - halfNum;
      var num = document.createElement('div');
      var mv = mvals[i];
      num.className = 'time-picker-number' + (tpSelectedMinute === mv ? ' selected' : '');
      num.textContent = mv < 10 ? '0' + mv : String(mv);
      num.style.left = x + 'px';
      num.style.top = y + 'px';
      num.style.width = numSize + 'px';
      num.style.height = numSize + 'px';
      num.style.lineHeight = numSize + 'px';
      num.setAttribute('data-minute', mv);
      num.onclick = (function(m) {
        return function() {
          tpSelectedMinute = m;
          renderTimePickerClock();
          updateTpSelected();
        };
      })(mv);
      clock.appendChild(num);
    }
    var ma = (tpSelectedMinute / 5) * 30;
    minuteHand.style.transform = 'rotate(' + ma + 'deg)';
    minuteHand.style.height = (radius - 5) + 'px';
  }
}

function updateTpSelected() {
  var hStr = tpSelectedHour < 10 ? '0' + tpSelectedHour : String(tpSelectedHour);
  var mStr = tpSelectedMinute < 10 ? '0' + tpSelectedMinute : String(tpSelectedMinute);
  document.getElementById('tpHour').textContent = hStr;
  document.getElementById('tpMinute').textContent = mStr;
  document.getElementById('tpAM').classList.toggle('active', tpPeriod === 'AM');
  document.getElementById('tpPM').classList.toggle('active', tpPeriod === 'PM');
}

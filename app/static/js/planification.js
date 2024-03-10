
      // JavaScript code to manage the lamp schedule
      var schedule = {};
    
      function toggleDay(btn, day) {
        btn.classList.toggle("active"); // Toggle the "active" class
        if (!schedule[day]) {
          schedule[day] = { on: null, off: null };
        } else {
          delete schedule[day]; // If the day is being deactivated, remove it from the schedule
        }
      }
    
      function applySchedule() {
        // Extract values from input fields
        var lamp = document.getElementById("lamp-selector").value;
        var timeOn = document.getElementById("time-on").value;
        var timeOff = document.getElementById("time-off").value;
    
        // Validation (optional): Check if timeOn is before timeOff. If not, alert the user.
    
        // Apply to active days
        var activeDaysButtons = document.querySelectorAll(".day-selector .day-btn.active");
        activeDaysButtons.forEach(function(dayBtn) {
          var day = dayBtn.innerText.trim().toLowerCase();
          schedule[day] = { on: timeOn, off: timeOff };
        });
    
        // Feedback to user that the schedule has been applied
        alert("Schedule applied for " + lamp);
    
        // Log the schedule to the console for debugging purposes
        console.log("Schedule for " + lamp + ":", schedule);
      }
    
      function saveSchedule() {
        // Implementation for saving the schedule could include sending the data to a server or saving to local storage
        // For demonstration, we'll simply log it to the console
    
        console.log("Schedule saved:", schedule);
        alert("Schedule saved successfully.");
    
        // Potentially stringify and save to local storage
        // localStorage.setItem('lampSchedule', JSON.stringify(schedule));
      }
    
  
  
    // JavaScript code to manage the lamp schedule
    var schedule = {};
  
    function toggleDay(btn, day) {
      // Functionality to toggle days and manage schedule
    }
  
    function applySchedule() {
      // Functionality to apply the schedule
    }
  
    function saveSchedule() {
      // Functionality to save the schedule
    }
  
    // Additional script omitted for brevity
  
  
      // JavaScript code to manage the lamp schedule
      var schedule = {};
    
      function toggleDay(btn, day) {
        btn.classList.toggle("active"); // Toggle the "active" class
        if (!schedule[day]) {
          schedule[day] = { on: null, off: null };
        } else {
          delete schedule[day]; // If the day is being deactivated, remove it from the schedule
        }
      }
    
      function applySchedule() {
        // Extract values from input fields
        var lamp = document.getElementById("lamp-selector").value;
        var timeOn = document.getElementById("time-on").value;
        var timeOff = document.getElementById("time-off").value;
    
        // Validation (optional): Check if timeOn is before timeOff. If not, alert the user.
    
        // Apply to active days
        var activeDaysButtons = document.querySelectorAll(".day-selector .day-btn.active");
        activeDaysButtons.forEach(function(dayBtn) {
          var day = dayBtn.innerText.trim().toLowerCase();
          schedule[day] = { on: timeOn, off: timeOff };
        });
    
        // Feedback to user that the schedule has been applied
        alert("Schedule applied for " + lamp);
    
        // Log the schedule to the console for debugging purposes
        console.log("Schedule for " + lamp + ":", schedule);
      }
    
      function saveSchedule() {
        // Implementation for saving the schedule could include sending the data to a server or saving to local storage
        // For demonstration, we'll simply log it to the console
    
        console.log("Schedule saved:", schedule);
        alert("Schedule saved successfully.");
    
        // Potentially stringify and save to local storage
        // localStorage.setItem('lampSchedule', JSON.stringify(schedule));
      }
    
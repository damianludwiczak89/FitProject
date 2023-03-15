document.addEventListener('DOMContentLoaded', function() {

    // Include sounds
    const audio = new Audio("https://www.fesliyanstudios.com/play-mp3/1805");
    const end_sound = new Audio("https://www.fesliyanstudios.com/play-mp3/864");

    // Hide stop and pause buttons
    document.querySelector('#stop').style.display = "none";
    document.querySelector('#pause').style.display = "none";
    document.querySelector('#congrats').style.display = "none";

    document.querySelector('#start').onclick = function () {
        // Start animation for work timer
        document.querySelector('#work').style.animationPlayState = "running";
        document.querySelector('#work').style.animationName = "grow";
        // Get variables from the form and show them on the page
        let interval = parseInt(document.querySelector('#id_interval').value);
        let work = parseInt(document.querySelector('#id_work').value);
        let rest = parseInt(document.querySelector('#id_rest').value);
        document.querySelector('#work').innerHTML = work;
        document.querySelector('#rest').innerHTML = rest;
        document.querySelector('#interval').innerHTML = interval;
        
        // Wrong input catch - only numbers higher than 0 allowed
        if (isNaN(work) || isNaN(rest) || isNaN(interval) || (work && rest && interval) < 1){
            document.querySelector('#work').style.display = "none";
            document.querySelector('#rest').style.display = "none";
            document.querySelector('#interval').style.display = "none";
            alert("Invalid input");
            return;
        }
        document.querySelector('#work').style.display = "block";
        document.querySelector('#rest').style.display = "block";
        document.querySelector('#interval').style.display = "block";

        // Function to finish both timers when interval counter is 0 - change colors, and stop intervals, change buttons, end sound
        // shrink animations, grow congrats
        function finish() {
            document.querySelector('#interval_desc').style.color = "#28de10";
            document.querySelector('#work_desc').style.color = "black";      
            clearInterval(work_interval);
            document.querySelector('#stop').style.display = "none";
            document.querySelector('#pause').style.display = "none";
            document.querySelector('#start').style.display = "block";
            document.querySelector('#congrats').style.display = "block";
            document.querySelector('#work').style.animationName = "shrink";
            document.querySelector('#rest').style.animationName = "shrink";
            document.querySelector('#congrats').style.animationPlayState = "running";

            end_sound.play();
            return;
        };

        // Function for a stop button
        function stop() {
                    // Set values back and turn off intervals, whichever is currently active, shrink animations
                    let interval = parseInt(document.querySelector('#id_interval').value);
                    let work = parseInt(document.querySelector('#id_work').value);
                    let rest = parseInt(document.querySelector('#id_rest').value);
                    document.querySelector('#work').style.animationName = "shrink";
                    document.querySelector('#rest').style.animationName = "shrink";
                    document.querySelector('#work').innerHTML = work;
                    document.querySelector('#rest').innerHTML = rest;
                    document.querySelector('#interval').innerHTML = interval;
                    document.querySelector('#interval_desc').style.color = "#black";
                    document.querySelector('#rest_desc').style.color = "black";
                    document.querySelector('#work_desc').style.color = "black";
                    document.querySelector('#start').style.display = "block";
                    document.querySelector('#pause').style.display = "none";
                    document.querySelector('#stop').style.display = "none";
                    document.querySelector('#pause').value = "Pause";
                    clearInterval(work_interval);
                    clearInterval(rest_interval);
                };

            // Function for a pause/continue button
            function pause() {

                // If button value is Continue
                if (document.querySelector('#pause').value === "Continue") {
                    document.querySelector('#pause').value = "Pause";

                        if (document.querySelector('#rest_desc').style.color === "black")
                            {
                            work_interval = setInterval(work_count, 1000);
                            }
                        
                            else {
                                rest_interval = setInterval(rest_count, 1000);
                            }
                        }
                // If button value is Pause
                else {
                document.querySelector('#pause').value = "Continue";
                clearInterval(work_interval);
                clearInterval(rest_interval);
                    }
            
        };
        
            // Function for a work timer
            function work_count() {

                // Stop button
                document.querySelector('#stop').onclick = function () {
                    stop();
                    return;
                };

                // Pause button
                document.querySelector('#pause').onclick = function () {
                    pause();
                };

                // 
                document.querySelector('#rest_desc').style.color = "black";
                document.querySelector('#work_desc').style.color = "#28de10";
            
                // Decrease work timer and update in html
                work--;
                document.querySelector('#work').innerHTML = work;
            
                // When work timer reaches zero, decrease interval count by 1, update in html, reset work timer, start rest timer
                // play sound
                if (work == 0) {
                    clearInterval(work_interval);
                    work = parseInt(document.querySelector('#id_work').value)
                    document.querySelector('#work').innerHTML = work;

                    

                    // If interval equals 1, its the end of both timers
                    if (interval === 1) {
                            document.querySelector('#interval').innerHTML = 0;
                            finish();
                            return;
                        }
                // Start animation for rest, shrink one, grow the other
                document.querySelector('#rest').style.animationPlayState = "running";
                document.querySelector('#rest').style.animationName = "grow";
                document.querySelector('#work').style.animationName = "shrink";
                audio.play();
                rest_interval = setInterval(rest_count, 1000);
                }
            }

            // Function for a rest timer
            function rest_count() {

                // Stop button
                document.querySelector('#stop').onclick = function () {

                    stop();
                    return;
                };

                // Pause button
                document.querySelector('#pause').onclick = function () {
                    pause();
                };


                document.querySelector('#work_desc').style.color = "black";
                document.querySelector('#rest_desc').style.color = "#28de10";
                
                // Decrease work timer and update in html
                rest--;
                document.querySelector('#rest').innerHTML = rest;
            
                
                // When rest timer reaches zero, decrease interval count by 1, update in html, reset rest timer, start work timer
                // play sound
                if (rest == 0) {
                    interval--;
                    document.querySelector('#interval').innerHTML = interval;
                    rest = parseInt(document.querySelector('#id_rest').value)
                    document.querySelector('#rest').innerHTML = rest;
                    clearInterval(rest_interval);
                    audio.play();
                    // Shrink one, grow the other
                    document.querySelector('#rest').style.animationName = "shrink";
                    document.querySelector('#work').style.animationName = "grow";
                    work_interval = setInterval(work_count, 1000);

                }
            }

            // Hide start button, display stop and pause buttons
            document.querySelector('#stop').style.display = "block";
            document.querySelector('#pause').style.display = "block";
            document.querySelector('#start').style.display = "none";
            document.querySelector('#congrats').style.display = "none";

            // Change interval color back to black in case it is not a first time being used
            document.querySelector('#interval_desc').style.color = "black";
    
            // Start the countdown
            work_interval = setInterval(work_count, 1000);

            
        return false;
    };
});
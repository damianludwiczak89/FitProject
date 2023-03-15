document.addEventListener('DOMContentLoaded', function() {
    // Hide form, hide single training display div
    document.querySelector('#form').style.display = "none";
    document.querySelector('#show').style.display = "none";
    document.querySelector('#delete').style.display = "none";

    // Delete button to show confirmation question
    document.querySelector('#delete_button').onclick = function () {
        if (document.querySelector('#delete').style.display === "none") {
            document.querySelector('#delete').style.display = "block";
        }
        else {
            document.querySelector('#delete').style.display = "none";
        }
    };
    
    // Button to hide single training
    document.querySelector('#hide').onclick = function () {
        document.querySelector('#show').style.display = "none";
        document.querySelector('#delete').style.display = "none";
    };

    // Button for displaying/hiding form
    document.querySelector('#add').onclick = function () {
        if (document.querySelector('#form').style.display === "none") {
            document.querySelector('#form').style.display = "block";
        }
        else {
            document.querySelector('#form').style.display = "none";
        }
    };

    // Displaying training on click
    document.querySelectorAll('.training-link').forEach(function(button) {

        button.onclick = function () {
            fetch('/training/'+button.dataset.id+'')
            .then(response => response.json())
            .then(training => {

                document.querySelector('#show').style.display = "block";
                document.querySelector("#training_name").innerHTML = `${training.day} ${training.time}: ${training.name}`;
                document.querySelector("#training_description").innerHTML = training.description;
                
                // Button to delete
                document.querySelector("#confirm_delete").onclick = function () {
                    fetch('/delete_training/'+button.dataset.id+'', { method: "DELETE" })
                    .then(() => 
                    document.querySelector("#training_name").innerHTML = "",
                    document.querySelector("#training_description").innerHTML = "",
                    document.querySelector('#show').style.display = "none",
                    document.querySelector('#delete').style.display = "none",
                    document.querySelector(`[data-id=${CSS.escape(button.dataset.id)}]`).innerHTML = ""
                    );
                }

    })}});
});
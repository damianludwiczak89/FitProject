document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#form').style.display = "none";
    document.querySelector('#show').style.display = "none";
    document.querySelector('#delete').style.display = "none";

    // Button to hide single cardio
    document.querySelector('#hide').onclick = function () {
        document.querySelector('#show').style.display = "none";
        document.querySelector('#delete').style.display = "none";
    };

    // Delete button to show confirmation question
    document.querySelector('#delete_button').onclick = function () {
        if (document.querySelector('#delete').style.display === "none") {
            document.querySelector('#delete').style.display = "block";
        }
        else {
            document.querySelector('#delete').style.display = "none";
        }
    };

    document.querySelector('#add').onclick = function () {
        if (document.querySelector('#form').style.display === "none") {
            document.querySelector('#form').style.display = "block";
        }
        else {
            document.querySelector('#form').style.display = "none";
        }
    };

    document.querySelectorAll('.link').forEach(function(button) {
        button.onclick = function () {
            fetch('/records/'+button.dataset.id+'')
            .then(response => response.json())
            .then(cardio => {

                document.querySelector('#show').style.display = "block";
                document.querySelector("#cardio_discipline").innerHTML = `${cardio.discipline} on ${cardio.date}`;
                document.querySelector("#cardio_description").innerHTML = `Covered ${cardio.distance} km in ${cardio.time} minutes`;

                // Button to delete
                document.querySelector("#confirm_delete").onclick = function () {
                    fetch('/delete_record/'+button.dataset.id+'', { method: "DELETE" })
                    .then(() => 
                    document.querySelector("#cardio_discipline").innerHTML = "",
                    document.querySelector("#cardio_description").innerHTML = "",
                    document.querySelector('#show').style.display = "none",
                    document.querySelector('#delete').style.display = "none",
                    document.querySelector(`[data-id=${CSS.escape(button.dataset.id)}]`).remove()
                    );
                }
            });
        }});
});
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
            fetch('/measurements/'+button.dataset.id+'')
            .then(response => response.json())
            .then(single_measurements => {


                if (single_measurements.thigh === null) {
                    single_measurements.thigh = ""
                }
                if (single_measurements.waist === null) {
                    single_measurements.waist = ""
                }
                if (single_measurements.chest === null) {
                    single_measurements.chest = ""
                }
                if (single_measurements.arm === null) {
                    single_measurements.arm = ""
                }
                if (single_measurements.notes === null) {
                    single_measurements.notes = ""
                }
                document.querySelector('#show').style.display = "block";
                document.querySelector("#measurements").innerHTML = `${single_measurements.date}:<br>
                <br>Weight: ${single_measurements.weight} kg<br>Waist: ${single_measurements.waist} cm<br>Chest: ${single_measurements.chest} cm
                <br>Thigh: ${single_measurements.thigh} cm<br>Arm: ${single_measurements.arm} cm<br><br>Notes: ${single_measurements.notes}`;


                // Button to delete
                document.querySelector("#confirm_delete").onclick = function () {
                    fetch('/delete_measurements/'+button.dataset.id+'', { method: "DELETE" })
                    .then(() => 
                    document.querySelector("#measurements").innerHTML = "",
                    document.querySelector('#show').style.display = "none",
                    document.querySelector('#delete').style.display = "none",
                    document.querySelector(`[data-id=${CSS.escape(button.dataset.id)}]`).remove()
                    );
                }
            });
        }});
});
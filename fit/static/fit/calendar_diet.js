document.addEventListener('DOMContentLoaded', function() {
    // Hide form, hide single meal display div
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

    // Button to hide single meal
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

    // Displaying meal on click
    document.querySelectorAll('.meal-link').forEach(function(button) {
        button.onclick = function () {
            fetch('/meal/'+button.dataset.id+'')
            .then(response => response.json())
            .then(meal => {

                document.querySelector('#show').style.display = "block";
                document.querySelector("#meal_name").innerHTML = `${meal.day} ${meal.time}: ${meal.name}`;
                document.querySelector("#meal_description").innerHTML = `${meal.description}`;

                // Button to delete
                document.querySelector("#confirm_delete").onclick = function () {
                    fetch('/delete_meal/'+button.dataset.id+'', { method: "DELETE" })
                    .then(() => 
                    document.querySelector("#meal_name").innerHTML = "",
                    document.querySelector("#meal_description").innerHTML = "",
                    document.querySelector('#show').style.display = "none",
                    document.querySelector('#delete').style.display = "none",
                    document.querySelector(`[data-id=${CSS.escape(button.dataset.id)}]`).innerHTML = ""
                    );
                }
    })}});
});
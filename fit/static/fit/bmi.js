document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('form').onsubmit = function () {

        // Hide previous result if it is not a first calculation
        document.querySelector('h3').style.display = "none";

        // get values from form
        let height = parseInt(document.querySelector('#id_height').value);
        let weight = parseInt(document.querySelector('#id_weight').value);

        // centimetres to metres
        height = height / 100;

        // calculate bmi with 3 decimal places
        bmi = weight / (height * height);
        bmi = bmi.toFixed(3);

        // Display result
        let result = document.querySelector('h3');
        result.innerHTML = bmi;
        result.style.display = "block";

        // Display result with a description and a font color accordingly
        let description;

        if (bmi < 16) {
            result.style.color = "red";
            description = " - Severe Thinnes";
        }
        else if (bmi < 17) {
            result.style.color = "orange";
            description = " - Moderate Thinnes";
        }
        else if (bmi < 18.5) {
            result.style.color = "rgba(220, 220, 32)";
            description = " - Mild Thinnes";
        }
        else if (bmi < 25) {
            result.style.color = "green";
            description = " - Normal";
        }
        else if (bmi < 30) {
            result.style.color = "rgba(220, 220, 32)";
            description = " - Overweight";
        }
        else if (bmi < 35) {
            result.style.color = "orange";
            description = " - Obese Class I";
        }
        else if (bmi < 40) {
            result.style.color = "red";
            description = " - Obese Class II";
        }
        else {
            result.style.color = "#b10606";
            description = " - Obese Class III";
        }

        result.append(description);

        // return false to not reload the page
        return false;
        
    };
});
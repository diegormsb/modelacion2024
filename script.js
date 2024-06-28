document.addEventListener("DOMContentLoaded", function() {
    const aeropuertos = {
        "CCS": "Caracas",
        "AUA": "Aruba",
        "BON": "Bonaire",
        "CUR": "Curacao",
        "SXM": "St. Maarten",
        "SDQ": "Santo Domingo",
        "SBH": "St. Barths",
        "POS": "Port of Spain",
        "BGI": "Bridgetown",
        "FDF": "Fort-de-France",
        "PTP": "Pointe-à-Pitre"
    };
    const requerimientosVisa = {
        "CCS": false, "AUA": true, "BON": true, "CUR": true, "SXM": true,
        "SDQ": true, "SBH": false, "POS": false, "BGI": false, "FDF": false, "PTP": false
    };

    const visaSelect = document.getElementById("visa");
    const origenSelect = document.getElementById("origen");
    const destinoSelect = document.getElementById("destino");

    // Inicialmente deshabilitar los selects de aeropuertos
    origenSelect.disabled = true;
    destinoSelect.disabled = true;

    // Rellenar los selects de aeropuertos
    function rellenarSelects() {
        origenSelect.innerHTML = '<option value="" disabled selected>Seleccione...</option>';
        destinoSelect.innerHTML = '<option value="" disabled selected>Seleccione...</option>';

        for (const codigo in aeropuertos) {
            const nombreCompleto = `${codigo} - ${aeropuertos[codigo]}`;

            const optionOrigen = document.createElement("option");
            optionOrigen.value = codigo;
            optionOrigen.textContent = nombreCompleto;
            origenSelect.appendChild(optionOrigen);

            const optionDestino = document.createElement("option");
            optionDestino.value = codigo;
            optionDestino.textContent = nombreCompleto;
            destinoSelect.appendChild(optionDestino);
        }
    }

    rellenarSelects();

    visaSelect.addEventListener("change", function() {
        const visa = visaSelect.value;
        origenSelect.disabled = false;  // Habilitar el select de origen cuando se seleccione la visa

        origenSelect.querySelectorAll("option").forEach(option => {
            if (visa === "no" && requerimientosVisa[option.value]) {
                option.disabled = true;
            } else {
                option.disabled = false;
            }
        });

        // Resetear el valor de origen y destino al cambiar la visa
        origenSelect.value = "";
        destinoSelect.value = "";
        destinoSelect.disabled = true;  // Deshabilitar destino hasta que se seleccione origen
    });

    origenSelect.addEventListener("change", function() {
        const origen = origenSelect.value;
        destinoSelect.disabled = false;  // Habilitar el select de destino cuando se seleccione el origen
        
        destinoSelect.querySelectorAll("option").forEach(option => {
            if (option.value === origen) {
                option.disabled = true;
            } else {
                option.disabled = false;
            }
        });

        destinoSelect.value = "";
        document.getElementById("origin").textContent = origen;  // Actualizar el campo de origen con el código
    });

    destinoSelect.addEventListener("change", function() {
        const destino = destinoSelect.value;
        document.getElementById("destination").textContent = destino;  // Actualizar el campo de destino con el código
    });

    document.getElementById("flightForm").addEventListener("submit", function(event) {
        event.preventDefault();
        const origen = origenSelect.value;
        const destino = destinoSelect.value;
        const visa = visaSelect.value === "si";
        const preferencia = document.getElementById("preferencia").value;

        fetch(`http://localhost:8000/?origen=${origen}&destino=${destino}&visa=${visa}&preferencia=${preferencia}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById("result").textContent = data.result || data.error;
                document.getElementById("airline").textContent = "UWU";
                document.getElementById("origin").textContent = origen;
                document.getElementById("destination").textContent = destino;
                document.getElementById("passenger").textContent = document.getElementById("passenger").textContent;
            })
            .catch(error => {
                document.getElementById("result").textContent = "Ocurrió un error: " + error;
            });
    });
});

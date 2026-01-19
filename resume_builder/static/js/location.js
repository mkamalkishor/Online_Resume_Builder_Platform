const apiKey = "6217cca4a57004f301a5064141265a68dabf54ebada158106a06de25841e7744";

const countrySelect = document.getElementById("country");
const stateSelect = document.getElementById("state");
const citySelect = document.getElementById("city");

/* LOAD COUNTRIES */
fetch("https://api.countrystatecity.in/v1/countries", {
    headers: { "X-CSCAPI-KEY": "6217cca4a57004f301a5064141265a68dabf54ebada158106a06de25841e7744" }
})
    .then(res => res.json())
    .then(data => {
        data.forEach(country => {
            countrySelect.innerHTML +=
                `<option value="${country.iso2}">${country.name}</option>`;
        });
    });

/* LOAD STATES */
countrySelect.addEventListener("change", () => {
    stateSelect.innerHTML = `<option>Select State</option>`;
    citySelect.innerHTML = `<option>Select City</option>`;

    fetch(`https://api.countrystatecity.in/v1/countries/${countrySelect.value}/states`, {
        headers: { "X-CSCAPI-KEY": "6217cca4a57004f301a5064141265a68dabf54ebada158106a06de25841e7744" }
    })
        .then(res => res.json())
        .then(data => {
            data.forEach(state => {
                stateSelect.innerHTML +=
                    `<option value="${state.iso2}">${state.name}</option>`;
            });
        });
});

/* LOAD CITIES */
stateSelect.addEventListener("change", () => {
    citySelect.innerHTML = `<option>Select City</option>`;

    fetch(`https://api.countrystatecity.in/v1/countries/${countrySelect.value}/states/${stateSelect.value}/cities`, {
        headers: { "X-CSCAPI-KEY": "6217cca4a57004f301a5064141265a68dabf54ebada158106a06de25841e7744" }
    })
        .then(res => res.json())
        .then(data => {
            data.forEach(city => {
                citySelect.innerHTML +=
                    `<option value="${city.name}">${city.name}</option>`;
            });
        });
});

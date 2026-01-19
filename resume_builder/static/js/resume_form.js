let currentStep = 0;
const steps = document.querySelectorAll(".step");
const progress = document.getElementById("progressBar");
const submitBtn = document.getElementById("submitBtn");

function showStep(n) {
    steps.forEach(step => step.classList.add("d-none"));
    steps[n].classList.remove("d-none");
    progress.style.width = ((n + 1) / steps.length) * 100 + "%";

    if (n === steps.length - 1) {
        submitBtn.classList.remove("d-none");
    } else {
        submitBtn.classList.add("d-none");
    }
}

function nextStep() {
    if (currentStep < steps.length - 1) {
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 0) {
        currentStep--;
        showStep(currentStep);
    }
}

showStep(currentStep);

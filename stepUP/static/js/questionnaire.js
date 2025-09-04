let currentStep = 1;
const totalSteps = 6;

function updateProgress() {
    const percentage = (currentStep / totalSteps) * 100;
    document.getElementById('progressBar').style.width = percentage + '%';
    document.getElementById('progressBar').textContent = Math.round(percentage) + '%';
    document.getElementById('currentStep').textContent = currentStep;
}

function validateCurrentStep() {
    const activeStep = document.querySelector('.form-step.active');
    const requiredInputs = activeStep.querySelectorAll('input[required], select[required]');

    for (let input of requiredInputs) {
        if (!input.value.trim()) {
            input.focus();
            input.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return false;
        }
    }
    return true;
}

function nextStep() {
    if (!validateCurrentStep()) {
        return;
    }

    if (currentStep < totalSteps) {
        document.querySelector('.form-step.active').classList.remove('active');
        currentStep++;
        document.querySelector(`[data-step="${currentStep}"]`).classList.add('active');
        updateProgress();
        document.querySelector('.questionnaire-container').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function prevStep() {
    if (currentStep > 1) {
        document.querySelector('.form-step.active').classList.remove('active');
        currentStep--;
        document.querySelector(`[data-step="${currentStep}"]`).classList.add('active');
        updateProgress();
        document.querySelector('.questionnaire-container').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Allow Enter key to go to next step
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            if (currentStep < totalSteps) {
                nextStep();
            }
        }
    });

    // Form submission validation
    document.getElementById('fitnessForm').addEventListener('submit', function(e) {
        if (!validateCurrentStep()) {
            e.preventDefault();
        }
    });

    // Initialize progress bar
    updateProgress();
});
/* SmartCredit AI - New Prediction Form Logic */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('predictionForm');
  if (!form) return;

  const formView = document.getElementById('formView');
  const loadingView = document.getElementById('loadingView');
  const loadingText = document.getElementById('loadingText');
  const predictBtn = document.getElementById('predictBtn');

  const loadingSteps = [
    'Validating applicant data...',
    'Encoding categorical features...',
    'Running ensemble model inference...',
    'Computing explainability factors...',
    'Finalising risk classification...',
  ];

  function clearErrors() {
    form.querySelectorAll('.form-control').forEach((el) => el.classList.remove('is-invalid'));
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearErrors();

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    // Basic client-side required check
    let firstInvalid = null;
    form.querySelectorAll('[required]').forEach((el) => {
      if (!el.value || !el.value.toString().trim()) {
        el.classList.add('is-invalid');
        if (!firstInvalid) firstInvalid = el;
      }
    });
    if (firstInvalid) {
      firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
      window.showToast('Please fill in all required fields.', 'danger');
      return;
    }

    predictBtn.disabled = true;
    formView.style.display = 'none';
    loadingView.style.display = 'block';

    let stepIdx = 0;
    const stepInterval = setInterval(() => {
      stepIdx = (stepIdx + 1) % loadingSteps.length;
      loadingText.textContent = loadingSteps[stepIdx];
    }, 550);

    try {
      const resp = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await resp.json();

      clearInterval(stepInterval);

      if (!data.success) {
        loadingView.style.display = 'none';
        formView.style.display = 'block';
        predictBtn.disabled = false;
        (data.errors || ['Something went wrong.']).forEach((err) => window.showToast(err, 'danger'));
        return;
      }

      // Small delay so the loading animation feels intentional, then redirect
      setTimeout(() => {
        window.location.href = `/predict/result/${data.result.prediction_id}`;
      }, 500);
    } catch (err) {
      clearInterval(stepInterval);
      loadingView.style.display = 'none';
      formView.style.display = 'block';
      predictBtn.disabled = false;
      window.showToast('Network error. Please try again.', 'danger');
    }
  });
});

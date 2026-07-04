/* SmartCredit AI - Prediction History Logic */

window.deletePrediction = async function (id) {
  if (!confirm('Delete this prediction? This cannot be undone.')) return;

  try {
    const resp = await fetch(`/api/history/${id}`, { method: 'DELETE' });
    const data = await resp.json();
    if (data.success) {
      const row = document.getElementById(`row-${id}`);
      if (row) {
        row.style.transition = 'opacity .3s ease';
        row.style.opacity = '0';
        setTimeout(() => row.remove(), 300);
      }
      window.showToast('Prediction deleted successfully.', 'success');
    } else {
      window.showToast('Could not delete this prediction.', 'danger');
    }
  } catch (err) {
    window.showToast('Network error while deleting.', 'danger');
  }
};

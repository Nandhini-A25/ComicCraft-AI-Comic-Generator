const form = document.getElementById('comic-form');
if (form) {
  form.addEventListener('submit', () => {
    const button = form.querySelector('button[type="submit"]');
    if (button) {
      button.disabled = true;
      button.textContent = 'Generating with AI…';
    }
  });
}

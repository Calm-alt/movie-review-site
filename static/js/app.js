document.addEventListener('DOMContentLoaded', () => {
  const toggleFormBtn = document.getElementById('toggle-form');
  const form = document.getElementById('review-form');
  const formHeading = document.getElementById('form-heading');
  const submitBtn = document.getElementById('submit-btn');
  const cancelBtn = document.getElementById('cancel-edit-btn');
  const titleInput = document.getElementById('title');
  const categoryInput = document.getElementById('category');
  const summaryInput = document.getElementById('summary');
  const detailsInput = document.getElementById('details');
  const defaultAction = form.getAttribute('action');

  function openForm() {
    form.classList.add('open');
    toggleFormBtn.textContent = 'Close';
  }

  function closeForm() {
    form.classList.remove('open');
    toggleFormBtn.textContent = '+ New Review';
  }

  function resetToAddMode() {
    form.setAttribute('action', defaultAction);
    formHeading.textContent = 'Log a new review';
    submitBtn.textContent = 'Post Review';
    cancelBtn.classList.remove('visible');
    form.reset();
  }

  toggleFormBtn.addEventListener('click', () => {
    if (form.classList.contains('open')) {
      closeForm();
      resetToAddMode();
    } else {
      resetToAddMode();
      openForm();
    }
  });

  cancelBtn.addEventListener('click', () => {
    resetToAddMode();
    closeForm();
  });

  document.querySelectorAll('.edit-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const card = btn.closest('.row');
      form.setAttribute('action', `/update/${card.dataset.id}`);
      titleInput.value = card.dataset.title;
      categoryInput.value = card.dataset.category;
      summaryInput.value = card.dataset.summary;
      detailsInput.value = card.dataset.details;
      formHeading.textContent = 'Edit review';
      submitBtn.textContent = 'Save Changes';
      cancelBtn.classList.add('visible');
      openForm();
      form.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  document.querySelectorAll('.show-more-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const details = document.getElementById(targetId);
      const isOpen = details.classList.toggle('open');
      btn.textContent = isOpen ? 'Show less \u25B4' : 'Show more \u25BE';
    });
  });

  document.querySelectorAll('.delete-form').forEach((deleteForm) => {
    deleteForm.addEventListener('submit', (e) => {
      if (!confirm('Delete this review? This can\'t be undone.')) {
        e.preventDefault();
      }
    });
  });
});

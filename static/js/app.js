document.addEventListener('DOMContentLoaded', () => {
  const toggleFormBtn = document.getElementById('toggle-form');
  const form = document.getElementById('review-form');
  const formHeading = document.getElementById('form-heading');
  const submitBtn = document.getElementById('submit-btn');
  const cancelBtn = document.getElementById('cancel-edit-btn');
  const titleInput = document.getElementById('title');
  const categoryInput = document.getElementById('category');
  const mediaTypeInput = document.getElementById('media_type');
  const summaryInput = document.getElementById('summary');
  const detailsInput = document.getElementById('details');
  const defaultAction = form.getAttribute('action');

  const starPicker = document.getElementById('star-picker');
  const starPickerFg = document.getElementById('star-picker-fg');
  const ratingInput = document.getElementById('rating');

  function renderStarPicker(value) {
    const pct = value ? (value / 5) * 100 : 0;
    starPickerFg.style.width = `${pct}%`;
    starPicker.setAttribute('aria-valuenow', value || 0);
    starPicker.setAttribute('aria-label', value ? `Star rating: ${value} out of 5` : 'Star rating: none set');
  }

  function ratingFromEvent(e) {
    const bg = starPicker.querySelector('.stars-bg');
    const rect = bg.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const frac = Math.min(Math.max((clientX - rect.left) / rect.width, 0), 1);
    return Math.round(frac * 5 * 2) / 2;
  }

  function setRating(value) {
    ratingInput.value = value ? value : '';
    renderStarPicker(value);
  }

  if (starPicker) {
    starPicker.addEventListener('mousemove', (e) => {
      renderStarPicker(ratingFromEvent(e));
    });

    starPicker.addEventListener('mouseleave', () => {
      renderStarPicker(parseFloat(ratingInput.value) || 0);
    });

    starPicker.addEventListener('click', (e) => {
      setRating(ratingFromEvent(e));
    });

    starPicker.addEventListener('keydown', (e) => {
      const current = parseFloat(ratingInput.value) || 0;
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
        e.preventDefault();
        setRating(Math.min(5, current + 0.5));
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
        e.preventDefault();
        setRating(Math.max(0, current - 0.5));
      }
    });
  }

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
    if (starPicker) setRating(0);
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
      mediaTypeInput.value = card.dataset.mediaType;
      summaryInput.value = card.dataset.summary;
      detailsInput.value = card.dataset.details;
      if (starPicker) setRating(parseFloat(card.dataset.rating) || 0);
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

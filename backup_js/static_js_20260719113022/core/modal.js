// Modal helpers
export function openModal(selector) {
  const modal = document.querySelector(selector);
  if (modal) modal.classList.remove('hidden');
}

export function closeModal(selector) {
  const modal = document.querySelector(selector);
  if (modal) modal.classList.add('hidden');
}

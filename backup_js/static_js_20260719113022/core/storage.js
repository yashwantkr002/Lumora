// Local storage helpers
export function saveItem(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

export function loadItem(key, fallback = null) {
  const item = localStorage.getItem(key);
  return item ? JSON.parse(item) : fallback;
}

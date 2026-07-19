// Intersection observer helpers
export function observeElement(element, callback) {
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => entry.isIntersecting && callback(entry));
    });
    observer.observe(element);
  }
}

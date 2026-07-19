// Shared API helpers
export const api = {
  get: async (url, options = {}) => fetch(url, { ...options, method: 'GET' }),
  post: async (url, options = {}) => fetch(url, { ...options, method: 'POST' }),
};

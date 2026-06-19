import apiClient from './client';

export const authAPI = {
  register: (data) => apiClient.post('/api/auth/register', data),
  login: (data) => apiClient.post('/api/auth/login-json', data),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
  getMe: () => apiClient.get('/api/auth/me'),
};

export const booksAPI = {
  getAll: (params) => apiClient.get('/api/book-club/books', { params }),
  create: (data) => apiClient.post('/api/book-club/books', data),
};

export const eventsAPI = {
  getAll: (params) => apiClient.get('/api/book-club/events', { params }),
  getById: (id) => apiClient.get(`/api/book-club/events/${id}`),
  create: (data) => apiClient.post('/api/book-club/events', data),
  delete: (id) => apiClient.delete(`/api/book-club/events/${id}`),
};

export const bookingsAPI = {
  create: (data) => apiClient.post('/api/book-club/bookings', data),
  getMy: () => apiClient.get('/api/book-club/my-bookings'),
  cancel: (id) => apiClient.delete(`/api/book-club/bookings/${id}`),
};


export const adminAPI = {
  getStats: () => apiClient.get('/api/book-club/admin/stats'),
};


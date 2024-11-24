export const API_BASE_URL = 'http://localhost:8000';

export const API_ROUTES = {
  LOGIN: '/users/login',
  SIGNUP: '/users/signup',
  FORGOT_PASSWORD: '/users/forgot_password',
  SHOPS_NUMBER : '/admin/get_number_shops',
  REVENUE_CURRENT : '/admin/get_current_revenue',
  USERS_NUMBER : '/admin/get_number_user',
  INCOME_STATS : '/admin/statistics_income',
  CAT_STATS : '/admin/statistics_category',
  ORDER_STATS : '/admin/statistics_number_orders',
  CREATE_ADMIN : '/admin/create_admin',
  GET_GOOGLE_LOGIN: '/users/get_google_login',
  CHAT_MESSAGE: '/ai/chatbot',
};

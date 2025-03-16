class ApiConstants {
  // Base URL for Fake Store API
  static const String baseUrl = 'https://fakestoreapi.com';

  // Product endpoints
  static const String productsEndpoint = '/products';
  static const String productCategoriesEndpoint = '/products/categories';

  // Authentication endpoints
  static const String loginEndpoint = '/auth/login';
  static const String registerEndpoint = '/users';

  // Pagination and Sorting
  static const int defaultPageLimit = 10;
  static const String sortAscending = 'asc';
  static const String sortDescending = 'desc';
} 
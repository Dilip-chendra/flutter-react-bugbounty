import 'package:flutter/foundation.dart';

import '../../domain/entities/product_entity.dart';
import '../../domain/usecases/get_products_usecase.dart';

class ProductProvider with ChangeNotifier {
  final GetProductsUseCase getProductsUseCase;
  final GetProductByIdUseCase getProductByIdUseCase;
  final GetProductCategoriesUseCase getCategoriesUseCase;
  final SearchProductsUseCase searchProductsUseCase;

  ProductProvider({
    required this.getProductsUseCase,
    required this.getProductByIdUseCase,
    required this.getCategoriesUseCase,
    required this.searchProductsUseCase,
  });

  List<ProductEntity> _products = [];
  List<ProductEntity> _searchResults = [];
  List<String> _categories = [];
  ProductEntity? _selectedProduct;
  bool _isLoading = false;
  String? _error;

  int _currentPage = 1;
  bool _hasMoreProducts = true;

  // Getters
  List<ProductEntity> get products => _products;
  List<ProductEntity> get searchResults => _searchResults;
  List<String> get categories => _categories;
  ProductEntity? get selectedProduct => _selectedProduct;
  bool get isLoading => _isLoading;
  String? get error => _error;

  // Fetch Products
  Future<void> fetchProducts({
    int limit = 10,
    int page = 1,
    String? category,
    String? sort,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final fetchedProducts = await getProductsUseCase(
        limit: limit,
        page: page,
        category: category,
        sort: sort,
      );

      // If it's the first page, replace the list. Otherwise, append.
      if (page == 1) {
        _products = fetchedProducts;
      } else {
        _products.addAll(fetchedProducts);
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Get Product by ID
  Future<void> fetchProductById(int id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _selectedProduct = await getProductByIdUseCase(id);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Fetch Categories
  Future<void> fetchCategories() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _categories = await getCategoriesUseCase();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Search Products
  Future<void> searchProducts(String query) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _searchResults = await searchProductsUseCase(query);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Clear search results
  void clearSearchResults() {
    _searchResults = [];
    notifyListeners();
  }
} 
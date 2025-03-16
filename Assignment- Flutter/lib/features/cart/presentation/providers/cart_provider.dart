import 'package:flutter/foundation.dart';

import '../../domain/entities/cart_entity.dart';
import '../../domain/usecases/cart_usecases.dart';
import '../../../products/domain/entities/product_entity.dart';

class CartProvider with ChangeNotifier {
  final GetCartUseCase getCartUseCase;
  final AddToCartUseCase addToCartUseCase;
  final RemoveFromCartUseCase removeFromCartUseCase;
  final UpdateCartItemQuantityUseCase updateCartItemQuantityUseCase;
  final ClearCartUseCase clearCartUseCase;

  CartProvider({
    required this.getCartUseCase,
    required this.addToCartUseCase,
    required this.removeFromCartUseCase,
    required this.updateCartItemQuantityUseCase,
    required this.clearCartUseCase,
  });

  CartEntity _cart = const CartEntity();
  bool _isLoading = false;
  String? _error;

  // Getters
  CartEntity get cart => _cart;
  bool get isLoading => _isLoading;
  String? get error => _error;
  double get totalPrice => _cart.totalPrice;
  int get totalItems => _cart.totalItems;

  // Load Cart
  Future<void> loadCart() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _cart = await getCartUseCase();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  // Add to Cart
  Future<void> addToCart(ProductEntity product, {int quantity = 1}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _cart = await addToCartUseCase(product, quantity: quantity);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  // Remove from Cart
  Future<void> removeFromCart(ProductEntity product) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _cart = await removeFromCartUseCase(product);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  // Update Cart Item Quantity
  Future<void> updateCartItemQuantity(ProductEntity product, int quantity) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _cart = await updateCartItemQuantityUseCase(product, quantity);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  // Clear Cart
  Future<void> clearCart() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await clearCartUseCase();
      _cart = const CartEntity();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }
} 
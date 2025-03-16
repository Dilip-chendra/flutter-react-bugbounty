import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/cart_model.dart';

class CartLocalDataSource {
  final SharedPreferences sharedPreferences;

  CartLocalDataSource(this.sharedPreferences);

  static const _cartKey = 'cart_items';

  Future<CartModel> getCart() async {
    final cartJson = sharedPreferences.getString(_cartKey);
    if (cartJson != null) {
      final Map<String, dynamic> cartMap = json.decode(cartJson);
      return CartModel.fromJson(cartMap);
    }
    return CartModel(items: []);
  }

  Future<void> saveCart(CartModel cart) async {
    await sharedPreferences.setString(_cartKey, json.encode(cart.toJson()));
  }

  Future<void> clearCart() async {
    await sharedPreferences.remove(_cartKey);
  }
} 
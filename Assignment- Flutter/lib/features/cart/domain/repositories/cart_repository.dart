import '../entities/cart_entity.dart';
import '../../../products/domain/entities/product_entity.dart';

abstract class CartRepository {
  Future<CartEntity> getCart();
  Future<CartEntity> addToCart(ProductEntity product, {int quantity});
  Future<CartEntity> removeFromCart(ProductEntity product);
  Future<CartEntity> updateCartItemQuantity(ProductEntity product, int quantity);
  Future<void> clearCart();
} 
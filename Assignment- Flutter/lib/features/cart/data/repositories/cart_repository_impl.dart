import '../../domain/repositories/cart_repository.dart';
import '../../domain/entities/cart_entity.dart';
import '../../../products/domain/entities/product_entity.dart';
import '../../../products/data/models/product_model.dart';
import '../datasources/cart_local_datasource.dart';
import '../models/cart_model.dart';

class CartRepositoryImpl implements CartRepository {
  final CartLocalDataSource localDataSource;

  CartRepositoryImpl(this.localDataSource);

  @override
  Future<CartEntity> getCart() async {
    return await localDataSource.getCart();
  }

  @override
  Future<CartEntity> addToCart(ProductEntity product, {int quantity = 1}) async {
    final cart = await localDataSource.getCart();
    final updatedCart = cart.addItem(
      ProductModel.fromEntity(product),
      quantity: quantity,
    );
    await localDataSource.saveCart(updatedCart);
    return updatedCart;
  }

  @override
  Future<CartEntity> removeFromCart(ProductEntity product) async {
    final cart = await localDataSource.getCart();
    final updatedCart = cart.removeItem(
      ProductModel.fromEntity(product),
    );
    await localDataSource.saveCart(updatedCart);
    return updatedCart;
  }

  @override
  Future<CartEntity> updateCartItemQuantity(ProductEntity product, int quantity) async {
    final cart = await localDataSource.getCart();
    final updatedCart = cart.updateItemQuantity(
      ProductModel.fromEntity(product),
      quantity,
    );
    await localDataSource.saveCart(updatedCart);
    return updatedCart;
  }

  @override
  Future<void> clearCart() async {
    await localDataSource.clearCart();
  }
} 
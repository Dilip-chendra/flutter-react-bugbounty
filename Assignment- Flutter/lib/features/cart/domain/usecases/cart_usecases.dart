import '../repositories/cart_repository.dart';
import '../entities/cart_entity.dart';
import '../../../products/domain/entities/product_entity.dart';

class GetCartUseCase {
  final CartRepository repository;

  GetCartUseCase(this.repository);

  Future<CartEntity> call() async {
    return await repository.getCart();
  }
}

class AddToCartUseCase {
  final CartRepository repository;

  AddToCartUseCase(this.repository);

  Future<CartEntity> call(ProductEntity product, {int quantity = 1}) async {
    return await repository.addToCart(product, quantity: quantity);
  }
}

class RemoveFromCartUseCase {
  final CartRepository repository;

  RemoveFromCartUseCase(this.repository);

  Future<CartEntity> call(ProductEntity product) async {
    return await repository.removeFromCart(product);
  }
}

class UpdateCartItemQuantityUseCase {
  final CartRepository repository;

  UpdateCartItemQuantityUseCase(this.repository);

  Future<CartEntity> call(ProductEntity product, int quantity) async {
    return await repository.updateCartItemQuantity(product, quantity);
  }
}

class ClearCartUseCase {
  final CartRepository repository;

  ClearCartUseCase(this.repository);

  Future<void> call() async {
    await repository.clearCart();
  }
} 
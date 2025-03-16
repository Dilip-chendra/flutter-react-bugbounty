import 'package:equatable/equatable.dart';
import '../../../products/domain/entities/product_entity.dart';

class CartItemEntity extends Equatable {
  final ProductEntity product;
  final int quantity;

  const CartItemEntity({
    required this.product,
    required this.quantity,
  });

  double get totalPrice => product.price * quantity;

  CartItemEntity copyWith({
    ProductEntity? product,
    int? quantity,
  }) {
    return CartItemEntity(
      product: product ?? this.product,
      quantity: quantity ?? this.quantity,
    );
  }

  @override
  List<Object?> get props => [product, quantity];
}

class CartEntity extends Equatable {
  final List<CartItemEntity> items;

  const CartEntity({this.items = const []});

  double get totalPrice => 
    items.fold(0, (total, item) => total + item.totalPrice);

  int get totalItems => 
    items.fold(0, (total, item) => total + item.quantity);

  CartEntity addItem(ProductEntity product, {int quantity = 1}) {
    final existingItemIndex = items.indexWhere((item) => item.product.id == product.id);
    
    if (existingItemIndex != -1) {
      final updatedItems = List<CartItemEntity>.from(items);
      final existingItem = updatedItems[existingItemIndex];
      updatedItems[existingItemIndex] = existingItem.copyWith(
        quantity: existingItem.quantity + quantity,
      );
      return CartEntity(items: updatedItems);
    } else {
      return CartEntity(
        items: [...items, CartItemEntity(product: product, quantity: quantity)],
      );
    }
  }

  CartEntity removeItem(ProductEntity product) {
    return CartEntity(
      items: items.where((item) => item.product.id != product.id).toList(),
    );
  }

  CartEntity updateItemQuantity(ProductEntity product, int newQuantity) {
    return CartEntity(
      items: items.map((item) {
        return item.product.id == product.id
            ? item.copyWith(quantity: newQuantity)
            : item;
      }).toList(),
    );
  }

  @override
  List<Object?> get props => [items];
} 
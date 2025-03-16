import '../../../products/data/models/product_model.dart';
import '../../domain/entities/cart_entity.dart';

class CartItemModel extends CartItemEntity {
  const CartItemModel({
    required ProductModel product,
    required int quantity,
  }) : super(product: product, quantity: quantity);

  factory CartItemModel.fromJson(Map<String, dynamic> json) {
    return CartItemModel(
      product: ProductModel.fromJson(json['product']),
      quantity: json['quantity'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'product': (product as ProductModel).toJson(),
      'quantity': quantity,
    };
  }
}

class CartModel extends CartEntity {
  const CartModel({required List<CartItemModel> items}) : super(items: items);

  factory CartModel.fromJson(Map<String, dynamic> json) {
    return CartModel(
      items: (json['items'] as List)
          .map((item) => CartItemModel.fromJson(item))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'items': items.map((item) => (item as CartItemModel).toJson()).toList(),
    };
  }

  // Override methods to ensure we're using CartItemModel
  @override
  CartModel addItem(product, {int quantity = 1}) {
    final existingItemIndex = items.indexWhere((item) => item.product.id == product.id);
    
    if (existingItemIndex != -1) {
      final updatedItems = List<CartItemModel>.from(items as List<CartItemModel>);
      final existingItem = updatedItems[existingItemIndex];
      updatedItems[existingItemIndex] = CartItemModel(
        product: product,
        quantity: existingItem.quantity + quantity,
      );
      return CartModel(items: updatedItems);
    } else {
      return CartModel(
        items: [...items as List<CartItemModel>, CartItemModel(product: product, quantity: quantity)],
      );
    }
  }

  @override
  CartModel removeItem(product) {
    return CartModel(
      items: items.where((item) => item.product.id != product.id).toList() as List<CartItemModel>,
    );
  }

  @override
  CartModel updateItemQuantity(product, int newQuantity) {
    return CartModel(
      items: items.map((item) {
        return item.product.id == product.id
            ? CartItemModel(product: product, quantity: newQuantity)
            : item,
      }).toList() as List<CartItemModel>,
    );
  }
} 
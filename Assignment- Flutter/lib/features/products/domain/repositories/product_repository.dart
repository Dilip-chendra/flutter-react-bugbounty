import '../entities/product_entity.dart';

abstract class ProductRepository {
  Future<List<ProductEntity>> getProducts({
    int limit = 10,
    int page = 1,
    String? category,
    String? sort,
  });

  Future<ProductEntity> getProductById(int id);

  Future<List<String>> getProductCategories();

  Future<List<ProductEntity>> searchProducts(String query);
} 
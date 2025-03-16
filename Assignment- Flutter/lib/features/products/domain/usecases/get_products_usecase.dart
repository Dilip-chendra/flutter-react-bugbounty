import '../entities/product_entity.dart';
import '../repositories/product_repository.dart';

class GetProductsUseCase {
  final ProductRepository repository;

  GetProductsUseCase(this.repository);

  Future<List<ProductEntity>> call({
    int limit = 10,
    int page = 1,
    String? category,
    String? sort,
  }) async {
    return await repository.getProducts(
      limit: limit,
      page: page,
      category: category,
      sort: sort,
    );
  }
}

class GetProductByIdUseCase {
  final ProductRepository repository;

  GetProductByIdUseCase(this.repository);

  Future<ProductEntity> call(int id) async {
    return await repository.getProductById(id);
  }
}

class GetProductCategoriesUseCase {
  final ProductRepository repository;

  GetProductCategoriesUseCase(this.repository);

  Future<List<String>> call() async {
    return await repository.getProductCategories();
  }
}

class SearchProductsUseCase {
  final ProductRepository repository;

  SearchProductsUseCase(this.repository);

  Future<List<ProductEntity>> call(String query) async {
    return await repository.searchProducts(query);
  }
} 
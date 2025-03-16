import '../../domain/repositories/product_repository.dart';
import '../../domain/entities/product_entity.dart';
import '../datasources/product_remote_datasource.dart';

class ProductRepositoryImpl implements ProductRepository {
  final ProductRemoteDataSource remoteDataSource;

  ProductRepositoryImpl(this.remoteDataSource);

  @override
  Future<List<ProductEntity>> getProducts({
    int limit = 10,
    int page = 1,
    String? category,
    String? sort,
  }) async {
    try {
      final products = await remoteDataSource.getProducts(
        limit: limit,
        page: page,
        category: category,
        sort: sort,
      );
      return products;
    } catch (e) {
      // Log error or handle specific exceptions
      rethrow;
    }
  }

  @override
  Future<ProductEntity> getProductById(int id) async {
    try {
      final product = await remoteDataSource.getProductById(id);
      return product;
    } catch (e) {
      // Log error or handle specific exceptions
      rethrow;
    }
  }

  @override
  Future<List<String>> getProductCategories() async {
    try {
      return await remoteDataSource.getProductCategories();
    } catch (e) {
      // Log error or handle specific exceptions
      rethrow;
    }
  }

  @override
  Future<List<ProductEntity>> searchProducts(String query) async {
    try {
      return await remoteDataSource.searchProducts(query);
    } catch (e) {
      // Log error or handle specific exceptions
      rethrow;
    }
  }
} 
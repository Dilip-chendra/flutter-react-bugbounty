import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_constants.dart';
import '../models/product_model.dart';

class ProductRemoteDataSource {
  final ApiClient apiClient;

  ProductRemoteDataSource(this.apiClient);

  Future<List<ProductModel>> getProducts({
    int limit = ApiConstants.defaultPageLimit,
    int page = 1,
    String? category,
    String? sort,
  }) async {
    String endpoint = ApiConstants.productsEndpoint;
    
    // Add query parameters
    final queryParams = <String, String>{
      'limit': limit.toString(),
      'page': page.toString(),
    };

    if (category != null) {
      queryParams['category'] = category;
    }

    if (sort != null) {
      queryParams['sort'] = sort;
    }

    final queryString = queryParams.entries
        .map((e) => '${e.key}=${e.value}')
        .join('&');

    final fullEndpoint = '$endpoint?$queryString';

    final response = await apiClient.get(fullEndpoint);

    return (response as List)
        .map((productJson) => ProductModel.fromJson(productJson))
        .toList();
  }

  Future<ProductModel> getProductById(int id) async {
    final response = await apiClient.get('${ApiConstants.productsEndpoint}/$id');
    return ProductModel.fromJson(response);
  }

  Future<List<String>> getProductCategories() async {
    final response = await apiClient.get(ApiConstants.productCategoriesEndpoint);
    return List<String>.from(response);
  }

  Future<List<ProductModel>> searchProducts(String query) async {
    final response = await apiClient.get(ApiConstants.productsEndpoint);
    
    return (response as List)
        .map((productJson) => ProductModel.fromJson(productJson))
        .where((product) => 
            product.title.toLowerCase().contains(query.toLowerCase()))
        .toList();
  }
} 
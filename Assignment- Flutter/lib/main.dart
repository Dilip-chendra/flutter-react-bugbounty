import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'core/network/api_client.dart';
import 'core/constants/api_constants.dart';

// Product Imports
import 'features/products/data/datasources/product_remote_datasource.dart';
import 'features/products/data/repositories/product_repository_impl.dart';
import 'features/products/domain/usecases/get_products_usecase.dart';
import 'features/products/presentation/providers/product_provider.dart';
import 'features/products/presentation/pages/home_page.dart';

// Auth Imports
import 'features/auth/data/datasources/auth_remote_datasource.dart';
import 'features/auth/data/repositories/auth_repository_impl.dart';
import 'features/auth/domain/usecases/auth_usecases.dart';
import 'features/auth/presentation/providers/auth_provider.dart';
import 'features/auth/presentation/pages/login_page.dart';

// Cart Imports
import 'features/cart/data/datasources/cart_local_datasource.dart';
import 'features/cart/data/repositories/cart_repository_impl.dart';
import 'features/cart/domain/usecases/cart_usecases.dart';
import 'features/cart/presentation/providers/cart_provider.dart';

void main() async {
  // Ensure Flutter is initialized
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize SharedPreferences
  final sharedPreferences = await SharedPreferences.getInstance();

  // Set up dependency injection
  final apiClient = ApiClient(ApiConstants.baseUrl);
  
  // Product Dependencies
  final productRemoteDataSource = ProductRemoteDataSource(apiClient);
  final productRepository = ProductRepositoryImpl(productRemoteDataSource);

  // Auth Dependencies
  final authRemoteDataSource = AuthRemoteDataSource(
    apiClient: apiClient,
    sharedPreferences: sharedPreferences,
  );
  final authRepository = AuthRepositoryImpl(authRemoteDataSource);

  // Cart Dependencies
  final cartLocalDataSource = CartLocalDataSource(sharedPreferences);
  final cartRepository = CartRepositoryImpl(cartLocalDataSource);

  runApp(
    MultiProvider(
      providers: [
        // Product Providers
        Provider<ApiClient>(create: (_) => apiClient),
        Provider<ProductRemoteDataSource>(
          create: (_) => productRemoteDataSource,
        ),
        Provider<ProductRepositoryImpl>(
          create: (_) => productRepository,
        ),
        ChangeNotifierProvider(
          create: (context) => ProductProvider(
            getProductsUseCase: GetProductsUseCase(productRepository),
            getProductByIdUseCase: GetProductByIdUseCase(productRepository),
            getCategoriesUseCase: GetProductCategoriesUseCase(productRepository),
            searchProductsUseCase: SearchProductsUseCase(productRepository),
          ),
        ),

        // Auth Providers
        Provider<AuthRemoteDataSource>(
          create: (_) => authRemoteDataSource,
        ),
        Provider<AuthRepositoryImpl>(
          create: (_) => authRepository,
        ),
        ChangeNotifierProvider(
          create: (context) => AuthProvider(
            loginUseCase: LoginUseCase(authRepository),
            registerUseCase: RegisterUseCase(authRepository),
            logoutUseCase: LogoutUseCase(authRepository),
            isLoggedInUseCase: IsLoggedInUseCase(authRepository),
            getCurrentUserUseCase: GetCurrentUserUseCase(authRepository),
          ),
        ),

        // Cart Providers
        Provider<CartLocalDataSource>(
          create: (_) => cartLocalDataSource,
        ),
        Provider<CartRepositoryImpl>(
          create: (_) => cartRepository,
        ),
        ChangeNotifierProvider(
          create: (context) => CartProvider(
            getCartUseCase: GetCartUseCase(cartRepository),
            addToCartUseCase: AddToCartUseCase(cartRepository),
            removeFromCartUseCase: RemoveFromCartUseCase(cartRepository),
            updateCartItemQuantityUseCase: UpdateCartItemQuantityUseCase(cartRepository),
            clearCartUseCase: ClearCartUseCase(cartRepository),
          ),
        ),
      ],
      child: const EcommerceApp(),
    ),
  );
}

class EcommerceApp extends StatelessWidget {
  const EcommerceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'E-Commerce App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: Consumer<AuthProvider>(
        builder: (context, authProvider, child) {
          return FutureBuilder<bool>(
            future: authProvider.checkLoginStatus(),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Scaffold(
                  body: Center(child: CircularProgressIndicator()),
                );
              }
              
              return authProvider.isLoggedIn ? const HomePage() : const LoginPage();
            },
          );
        },
      ),
    );
  }
} 
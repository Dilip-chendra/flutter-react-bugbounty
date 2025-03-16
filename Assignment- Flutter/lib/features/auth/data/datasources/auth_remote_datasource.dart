import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_constants.dart';
import '../models/user_model.dart';

class AuthRemoteDataSource {
  final ApiClient apiClient;
  final SharedPreferences sharedPreferences;

  AuthRemoteDataSource({
    required this.apiClient,
    required this.sharedPreferences,
  });

  Future<UserModel> login(String username, String password) async {
    final response = await apiClient.post(
      ApiConstants.loginEndpoint,
      body: {
        'username': username,
        'password': password,
      },
    );

    // Store token in shared preferences
    await sharedPreferences.setString('auth_token', response['token']);

    // Fetch user details
    final userResponse = await apiClient.get('/users/$username');
    final userModel = UserModel.fromJson({
      ...userResponse,
      'token': response['token'],
    });

    // Store user details
    await _cacheUserDetails(userModel);

    return userModel;
  }

  Future<UserModel> register({
    required String username,
    required String email,
    required String password,
    required String firstName,
    required String lastName,
    required String phone,
  }) async {
    final response = await apiClient.post(
      ApiConstants.registerEndpoint,
      body: {
        'username': username,
        'email': email,
        'password': password,
        'name': {
          'firstname': firstName,
          'lastname': lastName,
        },
        'phone': phone,
      },
    );

    final userModel = UserModel.fromJson({
      ...response,
      'token': '', // No token returned on registration
    });

    return userModel;
  }

  Future<void> logout() async {
    // Clear stored token and user details
    await sharedPreferences.remove('auth_token');
    await sharedPreferences.remove('user_id');
    await sharedPreferences.remove('username');
    await sharedPreferences.remove('email');
  }

  Future<bool> isLoggedIn() async {
    return sharedPreferences.getString('auth_token') != null;
  }

  Future<UserModel?> getCurrentUser() async {
    final token = sharedPreferences.getString('auth_token');
    if (token == null) return null;

    final userId = sharedPreferences.getInt('user_id');
    if (userId == null) return null;

    try {
      final userResponse = await apiClient.get('/users/$userId');
      return UserModel.fromJson({
        ...userResponse,
        'token': token,
      });
    } catch (e) {
      return null;
    }
  }

  Future<void> _cacheUserDetails(UserModel userModel) async {
    await sharedPreferences.setInt('user_id', userModel.id);
    await sharedPreferences.setString('username', userModel.username);
    await sharedPreferences.setString('email', userModel.email);
  }
} 
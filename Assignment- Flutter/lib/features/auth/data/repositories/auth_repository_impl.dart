import '../../domain/repositories/auth_repository.dart';
import '../../domain/entities/user_entity.dart';
import '../datasources/auth_remote_datasource.dart';

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;

  AuthRepositoryImpl(this.remoteDataSource);

  @override
  Future<UserEntity> login(String username, String password) async {
    try {
      return await remoteDataSource.login(username, password);
    } catch (e) {
      // Log error or handle specific exceptions
      rethrow;
    }
  }

  @override
  Future<UserEntity> register({
    required String username,
    required String email,
    required String password,
    required String firstName,
    required String lastName,
    required String phone,
  }) async {
    try {
      return await remoteDataSource.register(
        username: username,
        email: email,
        password: password,
        firstName: firstName,
        lastName: lastName,
        phone: phone,
      );
    } catch (e) {
      // Log error or handle specific exceptions
      rethrow;
    }
  }

  @override
  Future<void> logout() async {
    try {
      await remoteDataSource.logout();
    } catch (e) {
      // Log error or handle specific exceptions
      rethrow;
    }
  }

  @override
  Future<bool> isLoggedIn() async {
    try {
      return await remoteDataSource.isLoggedIn();
    } catch (e) {
      // Log error or handle specific exceptions
      return false;
    }
  }

  @override
  Future<UserEntity?> getCurrentUser() async {
    try {
      return await remoteDataSource.getCurrentUser();
    } catch (e) {
      // Log error or handle specific exceptions
      return null;
    }
  }
} 
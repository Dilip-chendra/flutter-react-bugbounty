import '../../domain/entities/user_entity.dart';

class UserModel extends UserEntity {
  const UserModel({
    required int id,
    required String username,
    required String email,
    required String firstName,
    required String lastName,
    required String phone,
    required String token,
  }) : super(
          id: id,
          username: username,
          email: email,
          firstName: firstName,
          lastName: lastName,
          phone: phone,
          token: token,
        );

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as int,
      username: json['username'] as String,
      email: json['email'] as String,
      firstName: json['name']['firstname'] as String,
      lastName: json['name']['lastname'] as String,
      phone: json['phone'] as String,
      token: json['token'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'name': {
        'firstname': firstName,
        'lastname': lastName,
      },
      'phone': phone,
      'token': token,
    };
  }
} 
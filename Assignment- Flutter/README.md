# Flutter E-Commerce Application

## Overview
This is a comprehensive e-commerce mobile application built using Flutter, following clean architecture principles and utilizing the Fake Store API.

## Features
- Product Listing with Infinite Scrolling
- Product Search Functionality
- Product Detail Page
- User Authentication
  - Login
  - Registration
  - Logout
- Cart Management
- Product Sorting and Filtering

## Authentication Flow
- Secure login and registration
- Form validation for registration
- Token-based authentication
- Persistent user sessions
- Error handling for authentication processes

## Prerequisites
- Flutter SDK (3.0.0 or higher)
- Dart SDK
- Android Studio or VS Code with Flutter extensions
- Git

## Setup and Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/ecommerce_app.git
cd ecommerce_app
```

2. Install dependencies
```bash
flutter pub get
```

3. Run the application
```bash
flutter run
```

## Project Structure
```
lib/
├── core/
│   ├── constants/
│   ├── errors/
│   └── network/
├── features/
│   ├── products/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   ├── auth/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── cart/
│       ├── data/
│       ├── domain/
│       └── presentation/
└── main.dart
```

## State Management
- Provider is used for state management
- Follows clean architecture with separation of concerns

## Authentication
- Implements secure user registration and login
- Uses Fake Store API for authentication
- Supports token-based authentication
- Persistent login state using SharedPreferences

## API
- Uses Fake Store API (https://fakestoreapi.com/)
- Implements comprehensive error handling
- Supports pagination and sorting

## Testing
- Unit tests for repositories and use cases
- Widget tests for UI components
- Authentication flow testing

## Dependencies
- provider: State management
- http: Network requests
- go_router: Navigation
- cached_network_image: Image caching
- form_validator: Form validation
- logger: Logging
- shared_preferences: Local storage
- equatable: Value equality

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/ecommerce_app](https://github.com/yourusername/ecommerce_app)

## Cart Management
- Add products to cart from product list and product details
- Remove products from cart
- Update cart item quantities
- Persistent cart storage using SharedPreferences
- Total price and item count calculations
- Error handling for cart operations
- Cart icon with item count in app bar
- Dismissible cart items
- Quantity selector in product details

## Cart Features
- Supports multiple cart items
- Prevents duplicate items
- Calculates total cart value
- Manages cart state with Provider
- Integrated with product pages
- Easy cart management 
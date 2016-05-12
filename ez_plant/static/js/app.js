// create the module and name it ez_plant
// var ez_plant = angular.module('ez_plant', ['ngRoute', '$http', 'AuthService']);
var ez_plant = angular.module('ez_plant', ['ngRoute']);

// configure our routes
ez_plant.config(function($routeProvider) {
  $routeProvider
     // route for the home page
     .when('/', {
         templateUrl : 'templates/home.html',
        //  controller  : 'loginController'
     })
     // route for the about page
     .when('/about', {
         templateUrl : 'templates/about.html',
         controller  : 'aboutController'
     })
     .when('/login', {
         templateUrl : 'templates/login.html',
         controller  : 'loginController'
     })
     .when('/register', {
         templateUrl : 'templates/register.html',
         controller  : 'registerController'
     })
});

ez_plant.controller('mainController', function($scope) {
   $scope.message = 'HOME PAGE!';
});

ez_plant.run(function ($rootScope, $location, $route, AuthService) {
  $rootScope.$on('$routeChangeStart', function (event, next, current) {
    if (AuthService.isLoggedIn() === false) {
      $location.path('/login');
      // $route.reload();
    }
  });
});
// https://realpython.com/blog/python/handling-user-authentication-with-angular-and-flask/

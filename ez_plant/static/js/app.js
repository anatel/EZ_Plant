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

ez_plant.controller('mainController', ['$scope', 'AuthService', '$location',
  function($scope, AuthService, $location) {
    $scope.logout = function(){
      // call logout from service
      AuthService.logout()
        .then(function () {
          $location.path('/login');
          return false;
        });
    }
}]);

ez_plant.run(function ($rootScope, $location, $route, AuthService) {
  $rootScope.$on('$routeChangeStart', function (event, next, current) {
    AuthService.isLoggedIn().then (function(){
      if (next.$$route.originalPath != '/register' && !AuthService.checkUser()) {
        $location.path('/login');
        // $route.reload();
      }
      else if (next.$$route.originalPath != '/login' && AuthService.checkUser())
      {
        $location.path('/');
      }
    });
  });
});
// https://realpython.com/blog/python/handling-user-authentication-with-angular-and-flask/

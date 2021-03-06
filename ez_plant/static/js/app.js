var ez_plant = angular.module('ez_plant', ['ngRoute']);

// configure our routes
ez_plant.config(function($routeProvider) {
  $routeProvider
     .when('/', {
         templateUrl : 'templates/garden.html',
         controller  : 'gardenController'
     })
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

/*Because Angular and Flask use the same symbols for binding, we chose to change
  Angular's default binding symbol to [[ ]], in order to prevent conflicts.*/
ez_plant.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

ez_plant.controller('mainController', ['$scope', 'AuthService', '$location',
  function($scope, AuthService, $location) {
    $scope.logout = function(){
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
      if (next && next.$$route.originalPath != '/register' && next.$$route.originalPath != '/about' && !AuthService.checkUser()) {
        $location.path('/login');
      }
    });
  });
});

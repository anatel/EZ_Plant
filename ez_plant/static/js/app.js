// create the module and name it ez_plant
var ez_plant = angular.module('ez_plant', ['ngRoute']);

// configure our routes
ez_plant.config(function($routeProvider) {
  $routeProvider
     // route for the home page
     .when('/', {
         templateUrl : 'templates/login.html',
         controller  : 'loginController'
     })
     // route for the about page
     .when('/about', {
         templateUrl : 'templates/about.html',
         controller  : 'aboutController'
     })
});

ez_plant.controller('mainController', function($scope) {
   $scope.message = 'HOME PAGE!';
});

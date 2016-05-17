// create the controller and inject Angular's $scope
var ez_plant = angular.module('ez_plant');

// ez_plant.controller('loginController', function($scope, $location, AuthService) {
ez_plant.controller('loginController',['$scope', 'AuthService', '$location',
 function($scope, AuthService, $location) {
  $scope.dataLoading = false;
  $scope.userDetails = {};
  $scope.showError = false;

  $scope.login = function () {
      // initial values
      $scope.dataLoading = true;

      // call login from service
      AuthService.login($scope.userDetails.username, $scope.userDetails.password)
        // handle success
        .then(function () {
          $location.path('/');
          $scope.dataLoading = false;
          $scope.loginForm = {};
        })
        // handle error
        .catch(function () {
          $scope.errorMessage = "Invalid username and/or password";
          $scope.showError = true;
          $scope.dataLoading = false;
          $scope.loginForm = {};
        });
    };
}]);
//TODO: http://cdn.rawgit.com/cornflourblue/angular-registration-login-example/master/login/login.controller.js

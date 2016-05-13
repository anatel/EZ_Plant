var ez_plant = angular.module('ez_plant');
ez_plant.controller('registerController',['$scope', 'AuthService', '$location',
 function($scope, AuthService, $location) {
  $scope.dataLoading = false;
  $scope.userDetails = {};
  $scope.showError = false;
  $scope.errorMessage;
  
  $scope.register = function () {
      // initial values
      $scope.dataLoading = true;
      $scope.showError = false;
      // call login from service
      AuthService.register($scope.userDetails)
        // handle success
        .then(function () {
          $location.path('/login');//TODO: show message on login page - account created successfuly, now you can login.
          $scope.dataLoading = false;
          $scope.registerForm = {};
        })
        // handle error
        .catch(function () {
          // $scope.errorMessage = "Invalid username and/or password";
          $scope.showError = true;
          $scope.dataLoading = false;
          $scope.registerForm = {};
        });
    };
}]);

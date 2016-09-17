var ez_plant = angular.module('ez_plant');
ez_plant.controller('registerController',['$scope', 'AuthService', '$location',
 function($scope, AuthService, $location) {
  $scope.dataLoading = false;
  $scope.userDetails = {};
  $scope.showError = false;
  $scope.errorMessage;

  $scope.register = function () {
      $scope.dataLoading = true;
      $scope.showError = false;

      AuthService.register($scope.userDetails)
        // handle success
        .then(function () {
          $location.path('/');
          $scope.dataLoading = false;
          $scope.registerForm = {};
        })
        // handle error
        .catch(function () {
          $scope.showError = true;
          $scope.dataLoading = false;
          $scope.registerForm = {};
        });
    };
}]);

var ez_plant = angular.module('ez_plant');

ez_plant.controller('loginController',['$scope', 'AuthService', '$location',
 function($scope, AuthService, $location) {
  $scope.dataLoading = false;
  $scope.userDetails = {};
  $scope.errorMessage = "";

  $scope.login = function () {
      $scope.dataLoading = true;
      var promise = AuthService.login($scope.userDetails.username, $scope.userDetails.password);
        promise.then(function(userObject){
          $location.path('/');
          $scope.dataLoading = false;
          $scope.errorMessage = '';
        }, function(errMsg){
          $scope.errorMessage = errMsg;
          $scope.dataLoading = false;
        });
    };
}]);

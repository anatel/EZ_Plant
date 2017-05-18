var ez_plant = angular.module('ez_plant');

ez_plant.controller('loginController',['$scope', 'AuthService', '$location',
 function($scope, AuthService, $location) {
  $scope.dataLoading = false;
  $scope.userDetails = {};
  $scope.errorMessage = "";

  $scope.login = function (demo) {
      $scope.dataLoading = true;

      if (demo) {
        $scope.userDetails.username = 'johndoe@test.com';
        $scope.userDetails.password = '123456';
      }

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

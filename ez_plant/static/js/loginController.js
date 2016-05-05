// create the controller and inject Angular's $scope
var ez_plant = angular.module('ez_plant');

ez_plant.controller('loginController', function($scope) {
  $scope.login = function() {
    alert("log in");
  };

});
//TODO: http://cdn.rawgit.com/cornflourblue/angular-registration-login-example/master/login/login.controller.js

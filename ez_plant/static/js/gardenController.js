var ez_plant = angular.module('ez_plant');

ez_plant.controller('gardenController', ['$scope', 'AuthService', function($scope, AuthService) {
  $scope.userDetails = AuthService.getUser();
  var plantsString = [{"name":"Plant1","type":"Rose","port_number":"A1","img_url":"static/assets/images/red-rose-plant.png","water_data":{"last_watered":"Sat Jul 23 2016 16:39:47"}},{"name":"Plant2","type":"Cactus","port_number":"A0","img_url":"static/assets/images/img-thing.jpg","water_data":{"last_watered":"Sat Jul 23 2016 16:50:47"}}];
  $scope.plants = plantsString;
  console.log($scope.plants);
}]);

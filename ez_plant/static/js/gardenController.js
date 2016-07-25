var ez_plant = angular.module('ez_plant');


ez_plant.controller('gardenController', ['$scope', 'AuthService', '$rootScope', function($scope, AuthService, $rootScope) {
  $scope.userDetails = AuthService.getUser();
  var plantsString =[{"plant_id":"a","name":"Plant1","type":"Rose","port_number":"A1","img_url":"static/assets/images/red-rose-plant.png","water_data":{"last_watered":"23/07/16 16:39"}},{"plant_id":"b","name":"Plant2","type":"Cactus","port_number":"A0","img_url":"static/assets/images/img-thing.jpg","water_data":{"last_watered":"23/07/17 17:00"}},{"plant_id":"c","name":"Lilu","type":"Lilac","port_number":"A4","img_url":"static/assets/images/lilac.jpg","water_data":{"last_watered":"23/07/18 17:00"}}];
  $scope.plants = plantsString;
  $scope.showForm = false;
  console.log($scope.plants);

  $scope.openPlantDetails = function(plantIndex){
    $scope.showForm = true;
    $scope.plant = plantIndex==undefined? {} : $scope.plants[plantIndex];
    placeArrow();

    $('html, body').animate({
        scrollTop: $(".plantDetailsWrapper").offset().top
    }, 2000);
  };




  function placeArrow()
  {
    var $thumbnail = $scope.plant.plant_id? $("#"+$scope.plant.plant_id ): $("#new");
    var $arrow = $(".arrow img");
    var pos = $thumbnail.offset();
    $scope.arrowPosLeft  = pos.left + $thumbnail.width()/2 - $arrow.width()/2;
  }
}]);

// ez_plant.controller('plantController', ['$scope', '$rootScope', function($scope, $rootScope) {
//
// }]);

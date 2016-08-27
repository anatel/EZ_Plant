var ez_plant = angular.module('ez_plant');


ez_plant.controller('gardenController', ['$scope', 'AuthService', '$rootScope', '$timeout', '$http', function($scope, AuthService, $rootScope, $timeout, $http) {
  $scope.userDetails = AuthService.getUser();
  $http({
      method : "GET",
      url : "/plants"
  }).then(function onSuccess(response) {
    console.log(response);
      $scope.plants = response.data.plants;
  }, function myError(response) {
      $scope.errMsg = 'There was an error loading plants';
      $("#errMsg").fadeIn("fast");
      console.log('error');
  });
  //var plantsString = [{"plant_id":"a","name":"Plant1","plant_type":"Rose","moisture_sensor_port":"A0","water_pump_port":2,"image_url":"static/assets/images/red-rose-plant.png","water_data":{"water_mode":"schedule","repeat_every":5,"hour":"14:00","last_watered":"23/07/16 16:39","next_watering":"23/07/16 16:39"}},{"plant_id":"b","name":"Plant2","plant_type":"Cactus","moisture_sensor_port":"A1","water_pump_port":3,"image_url":"static/assets/images/img-thing.jpg","water_data":{"water_mode":"moisture","low_threshold":50,"last_watered":"23/07/17 17:00"}},{"plant_id":"c","name":"Lilu","plant_type":"Lilac","moisture_sensor_port":"A2","water_pump_port":4,"image_url":"static/assets/images/lilac.jpg","water_data":{"water_mode":"moisture","low_threshold":20,"last_watered":"23/07/18 17:00"}}];
  //$scope.plants = plantsString;
  $scope.showForm = false;
  $scope.content = 'details';

  $scope.openPlantDetails = function(plantIndex){
    $scope.plantIndex = plantIndex;
    $scope.plant = plantIndex==undefined? {"water_data": { "water_mode": "schedule", "last_watered": "Never"}} : angular.copy($scope.plants[plantIndex]);
    if (plantIndex!=undefined && !$scope.plant.water_data.next_watering){
      $scope.calcNextWatering();
    }
    $http({
        method : "GET",
        url : "/get_free_ports"
    }).then(function onSuccess(response) {
        if (response.data){
          $scope.sensorPorts = response.data.free_moisture_ports;
          if ($scope.plant.moisture_sensor_port != undefined){
            $scope.sensorPorts.unshift($scope.plant.moisture_sensor_port);
          }
          $scope.pumpPorts = response.data.free_water_pump_ports;
          if ($scope.plant.water_pump_port != undefined){
            $scope.pumpPorts.unshift($scope.plant.water_pump_port);
          }
          $scope.showPlantDetails(plantIndex);
        }
        else {
          $scope.errMsg = 'There was an error loading plant\'s details...';
          $scope.handleAlerts('fail');
        }
    }, function myError(response) {
        $scope.errMsg = 'There was an error loading plant\'s details...';
        $scope.handleAlerts('fail');
        console.log('error');
    });
  };

  $scope.showPlantDetails = function(plantIndex){
    $scope.showForm = true;
    $scope.changeTabContent('details');
    $(".plantDetails").show();
    placeArrow();

    $('html, body').animate({
        scrollTop: $(".plantDetailsWrapper").offset().top
    }, 1000);
    $timeout(function () { $('.waterTime').timepicker({ 'timeFormat': 'H:i' }); $scope.plantForm.$setPristine();});

  }

  $scope.changeTabContent = function(tab){
    $scope.content = tab;
  };


  $scope.calcNextWatering = function(){
    days = $("#daysInput").val();
    hour = $("#hourInput").val();
    if (days != '')
    {
      var date = new Date();
      date.setDate(date.getDate() + parseInt(days));
      if (hour && hour != '')
      {
        hourArr = hour.split(':');
        date.setHours(parseInt(hourArr[0]));
        date.setMinutes(parseInt(hourArr[1]));
      }
      $scope.plant.water_data.next_watering = date;
    }
    else {
      $scope.plant.water_data.next_watering = '';
    }
  };

  //choose image dialog
  $scope.openDialog = function() {
    $("#inputId").click();
  };

  $scope.deletePlant = function(plantIndex)
  {
    var plantToDel = $scope.plants[plantIndex];
    if (confirm("Are you sure you want to delete plant: " + plantToDel.name + "?")){
      if ($scope.showForm)
      {
        $(".plantDetails").slideUp("slow",function(){
          $scope.showForm = false;
        });
      }
      $http({
          method : "DELETE",
          url : "/plants?plant_id="+plantToDel.plant_id
      }).then(function onSuccess(response) {
          $scope.plants.splice(plantIndex, 1);
          $scope.successMsg = "The plant: " + plantToDel.name + " was successfully deleted.";
          $scope.handleAlerts('success');
      }, function myError(response) {
          $scope.errMsg = 'There was an error deleting plant...';
          $scope.handleAlerts('fail');
          $timeout(function () { $("#errMsg").fadeOut("fast"); }, 5000);
          console.log('error');
      });
      $scope.plant = {};
    }
  }

  $scope.submitPlant = function() {
    console.log($scope.plant);
    var formData = new FormData();
    angular.forEach($scope.plant, function (value, key) {
        if (key == 'water_data'){
          value = JSON.stringify(value);
        }
        formData.append(key, value);
    });
    formData.append("file", $("#inputId")[0].files[0]);
    $http({
      method  : 'POST',
      url     : '/plants',
      data    : formData,  // pass in data as strings
      headers : { 'Content-Type': undefined }  // set the headers so angular passing info as form data (not request payload)
   })
   .then(function onSuccess(data) {
     console.log(data);
     if (data.data.result == 'success')
     {
       if ($scope.plantIndex != undefined){
         $scope.plants[$scope.plantIndex] = data.data.plant;
       } else {
         $scope.plants.push(data.data.plant);
       }
       $scope.successMsg = "Plant successfully submitted!";
       $scope.handleAlerts('success');
     }
   }, function onFailure(){
     $scope.errMsg = "An error occured while trying to submit plant...";
     $scope.handleAlerts('fail');
   });
  };

  $scope.handleAlerts = function(alertType){
    if (alertType == 'success'){
      $(".plantDetails").slideUp("slow",function(){
        $scope.showForm = false;
      });
      if($('#errMsg').length > 0)
      {
        $("#errMsg").fadeOut("fast");
      }
      $("#successMsg").fadeIn("fast");
      $timeout(function () { $("#successMsg").fadeOut("fast"); }, 5000);
    }
    else if (alertType == 'fail'){
      $("#errMsg").fadeIn("fast");
    }
  }

  //change plant photo
  $scope.readURL = function(input) {
    if (input.files && input.files[0]) {
      $("#submitPlantBtn").prop('disabled', false);
      var reader = new FileReader();
      reader.onload = function(e) {
        $('.imgContainer img')
          .attr('src', e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
    }
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

var ez_plant = angular.module('ez_plant');

ez_plant.controller('gardenController', ['$scope', 'AuthService', '$rootScope', '$timeout', '$http', function($scope, AuthService, $rootScope, $timeout, $http) {
  $scope.userDetails = AuthService.getUser();
  $http({
      method : "GET",
      url : "/plants"
  }).then(function onSuccess(response) {
    console.log(response);
      $scope.plants = response.data.plants;
      var shouldPoll = false;
      angular.forEach($scope.plants, function (plant, key) {
          if (plant.water_now == true) {
            shouldPoll = true;
          }
          if (plant.water_data.last_watered) {
            plant.water_data.last_watered = new Date(plant.water_data.last_watered);
          }
          if (plant.water_data.water_mode == 'schedule'){
            plant.water_data.hour = $scope.convertUTCHoursToLocalTimeZone(plant.water_data.hour);
            plant.water_data.next_watering = new Date(plant.water_data.next_watering);
          }
      });
      if (shouldPoll) {
        $scope.poll();
      }
  }, function onFailure(response) {
      $scope.errMsg = 'There was an error loading plants';
      $("#errMsg").fadeIn("fast");
      console.log('error');
  });
  $scope.showForm = false;
  $scope.content = 'details';

  $scope.openPlantDetails = function(plantIndex){
    $scope.plantIndex = plantIndex;
    $scope.plant = plantIndex==undefined? {"water_data": { "water_mode": "schedule", "last_watered": "Never"}} : angular.copy($scope.plants[plantIndex]);

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

  $scope.drawChart = function(){
    if (!$scope.googleLoad){
      google.charts.load('current', {packages: ['corechart', 'line']});
      $scope.googleLoad = true;
    }
    google.charts.setOnLoadCallback($scope.getPlantStats);
  };

  $scope.getPlantStats = function(){
    $http({
      method  : 'GET',
      url     : '/get_plant_stats?plant_id=' + $scope.plant.plant_id,
   })
   .then(
     function onSuccess(response) {
       console.log(response);
       var data = new google.visualization.DataTable();
       data.addColumn('datetime', 'Time');
       data.addColumn('number', 'Moisture %');

       stats_list = response.data.stats;
       stats_list.forEach(function(stats_pair) {
         stats_pair[0] = new Date(stats_pair[0]);
       })

       data.addRows(response.data.stats);
      //  $timeout(function () { $("#no_data_chart").animate({height: "28%"});}, 2000);

       $scope.chartNoData = response.data.stats.length == 0;
       var options = {
        titlePosition: 'none',
        backgroundColor: { fill:'transparent' },
        'width': 1000,
        'height': 480,
        pointSize: 4,
        // pointShape: 'star',
        hAxis: {
          title: 'Time'
        },
        vAxis: {
          title: 'Moisture %',
          minValue: 0,
          maxValue: 100
        },
        explorer: { actions: ['dragToZoom', 'rightClickToReset'], maxZoomIn: .03, zoomDelta: 0.5},
        colors: ['green']
      }
      var chart = new google.visualization.LineChart($("#plantStatsChart")[0]);
      chart.draw(data, options);
      $('html, body').animate({
        scrollTop: $(".plantDetailsWrapper").offset().top
      }, 200);
      $scope.refreshing = false;
      $scope.statsErr = false;
    },
    function onFailure(){
      $scope.refreshing = false;
      $scope.statsErr = true;
      $('html, body').animate({
        scrollTop: $(".plantDetailsWrapper").offset().top
      }, 200);
    });
  };

  $scope.showPlantDetails = function(){
    $scope.showForm = true;
    $scope.changeTabContent('details');
    $(".plantDetails").show();
    placeArrow();
    $("#submitPlantBtn").prop('disabled', true);
    $("#undoChangesBtn").prop('disabled', true);

    $('html, body').animate({
        scrollTop: $(".plantDetailsWrapper").offset().top
    }, 1000);
    $timeout(function () { $('.waterTime').timepicker({ 'timeFormat': 'H:i' }); $scope.plantForm.$setPristine();});

  };

  $scope.changeTabContent = function(tab){
    $scope.content = tab;
  };


  $scope.calcNextWatering = function(){
    days = $("#daysInput").val();
    hour = $("#hourInput").val();
    if (days != '')
    {
      var date = new Date();
      if (hour && hour != '')
      {
        hourArr = hour.split(':');
        if (date.getHours() > parseInt(hourArr[0]) ||
              (date.getHours() == parseInt(hourArr[0]) && date.getMinutes() >= parseInt(hourArr[1]))){
          date.setDate(date.getDate() + 1);
        }
        date.setHours(parseInt(hourArr[0]));
        date.setMinutes(parseInt(hourArr[1]));
      }
      else {
        date.setDate(date.getDate() + 1);
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
        if (key == 'water_data') {
          var newValue = angular.copy(value);
          delete newValue.last_watered; // it will be calculated on the client side for the server
          if (newValue.water_mode == 'schedule'){
            delete newValue.next_watering; //we dont send it to the server.
            //convert hour to UTC:
            newValue.hour = $scope.convertHoursToUTC(value.hour);
          }
          value = JSON.stringify(newValue);
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
       if ($scope.plant.water_data.water_mode == 'schedule'){
         data.data.plant.water_data.next_watering = new Date(data.data.plant.water_data.next_watering);
         data.data.plant.water_data.hour = $scope.convertUTCHoursToLocalTimeZone(data.data.plant.water_data.hour)
       }
       if ($scope.plantIndex != undefined){
         $scope.plants[$scope.plantIndex] = data.data.plant;
       } else {
         $scope.plants.push(data.data.plant);
       }

       if (data.data.plant.water_data.last_watered) {
         $scope.plant.water_data.last_watered = new Date(data.data.plant.water_data.last_watered);
         $scope.plants[$scope.plantIndex].water_data.last_watered = new Date(data.data.plant.water_data.last_watered);
       }
       $scope.successMsg = "Plant successfully submitted!";
       $scope.handleAlerts('success');
     }
   }, function onFailure(){
     $scope.errMsg = "An error occured while trying to submit plant...";
     $scope.handleAlerts('fail');
   });
  };

  $scope.convertHoursToUTC = function(hourStr) {
    var hourArr = hourStr.split(':');
    var hourInt = parseInt(hourArr[0]);
    var minInt = parseInt(hourArr[1]);
    var reqDate = new Date();
    reqDate.setMinutes(minInt);
    reqDate.setHours(hourInt);
    return reqDate.getUTCHours().toString() + ':' + reqDate.getUTCMinutes().toString();
  };

  $scope.convertUTCHoursToLocalTimeZone = function(hourStr){
    var hoursArr = hourStr.split(':');
    var hourInt = parseInt(hoursArr[0]);
    var minInt = parseInt(hoursArr[1]);
    var reqDate = new Date();
    reqDate.setUTCMinutes(minInt);
    reqDate.setUTCHours(hourInt);
    var hourStr = reqDate.getHours().toString();
    var minStr = reqDate.getMinutes().toString();
    return $scope.pad(hourStr) + ":" + $scope.pad(minStr);
  };

  $scope.pad = function(str) {
      if (parseInt(str) < 10) {
        return "0" + str;
      }
      return str;
  };

  $scope.waterNow = function(){
    if (confirm("Are you sure you want to water " + $scope.plant.name + " now?")) {
      $scope.loading(true);
      $http({
        method  : 'POST',
        url     : '/water_now?plant_id='+$scope.plant.plant_id,
     })
     .then(function onSuccess(response) {
       console.log(response);
       if (response.data.result == 'success')
       {
         $scope.plants[$scope.plantIndex].water_now = true;
         $scope.plant.water_now = true;

         $scope.loading(false);
         $scope.poll();
       }
     }, function onFailure(){
       $scope.loading(false);
       alert("There was an unexpected error.");
     });
    }
  }

  $scope.poll = function() {
    if (!$scope.polling){
      var intervalId = setInterval(function(){
        $http({
          method  : 'GET',
          url     : '/water_now',
       })
       .then(function onSuccess(response) {
         console.log(response);
         if (response.data.result == 'success'){
           var plantWaiting = false;
           angular.forEach($scope.plants, function(plant, index) {
             if (response.data.watering_data.hasOwnProperty(plant.plant_id)) {
               plant.water_now = response.data.watering_data[plant.plant_id].water_now;
               var lastWatered = response.data.watering_data[plant.plant_id].last_watered;
               plant.water_data.last_watered = lastWatered? new Date(lastWatered) : plant.water_data.last_watered;
               if (plant.plant_id == $scope.plant.plant_id) {
                 $scope.plant.water_now = plant.water_now;
                 $scope.plant.water_data.last_watered = plant.water_data.last_watered;
               }
               if (plant.water_now){
                 plantWaiting = true;
               }
             }
           });
           if (!plantWaiting) {
             clearInterval(intervalId);
             $scope.polling = false;
           }
           console.log($scope.plants);
         }
       }, function onFailure(){ //nothing should happen
         console.log('error getting water data');
       });
     }, 30*1000);
    }
  }

  $scope.loading = function(toggle) {
    $scope.isLoading = toggle;
  }

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
      $("#undoChangesBtn").prop('disabled', false);
      var reader = new FileReader();
      reader.onload = function(e) {
        $('.imgContainer img')
          .attr('src', e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
    }
  };

  $scope.undoChanges = function(){
    $scope.plantForm.$setPristine();
    $('#inputId').val("");
    $("#submitPlantBtn").prop('disabled', true);
    $("#undoChangesBtn").prop('disabled', true);
    if ($scope.plant.plant_id){
      $scope.plant = angular.copy($scope.plants[$scope.plantIndex]);
      if ($scope.plant.image_url) {
        $('.imgContainer img')
          .attr('src',$scope.plant.image_url);
      } else {
        $('.imgContainer img')
          .attr('src','static/assets/images/default_plant.png');
      }
    } else {
      $('.imgContainer img')
        .attr('src','static/assets/images/default_plant.png');
      $scope.plant = {"water_data": { "water_mode": "schedule", "last_watered": "Never"}};
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

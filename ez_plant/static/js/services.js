angular.module('ez_plant').factory('AuthService',
  ['$q', '$timeout','$http',
  function ($q, $timeout, $http) {
    // create user variable
    var user = null;
    // return available functions for use in controllers
    return ({
      isLoggedIn: isLoggedIn,
      login: login,
      logout: logout,
      register: register
  });

  function isLoggedIn() {
    console.log('user: ' + user);
    if(user) {
      return true;
    } else {
      return false;
    }
  }

  function login(username, password) {
  // create a new instance of deferred
    var deferred = $q.defer();

    // send a post request to the server
    $http.post('/login', {username: username, password: password})
      // handle success
      .success(function (data, status) {
        if(status === 200 && data.result){
          user = true;
          deferred.resolve();
        } else {
          user = false;
          deferred.reject();
        }
      })
    // handle error
      .error(function (data) {
        user = false;
        deferred.reject();
      });
      // return promise object
      return deferred.promise;
    }

    function logout() {
      // create a new instance of deferred
      var deferred = $q.defer();
      // send a get request to the server
      $http.get('/logout')
        // handle success
        .success(function (data) {
          user = false;
          deferred.resolve();
        })
        // handle error
        .error(function (data) {
          user = false;
          deferred.reject();
        });
      // return promise object
      return deferred.promise;
    }

    function register(user_data) {
      // create a new instance of deferred
      var deferred = $q.defer();
      // send a post request to the server
      $http.post('/register', user_data)
        // handle success
        .success(function (data, status) {
          if(status === 200 && data.result){
            deferred.resolve(data);
          } else {
            deferred.reject(data);
          }
        })
        // handle error
        .error(function (data) {
          deferred.reject(data);
        });
      // return promise object
      return deferred.promise;
    }
}]);

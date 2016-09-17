angular.module('ez_plant').factory('AuthService',
  ['$q', '$timeout','$http',
  function ($q, $timeout, $http) {
    var user = null;

    // return available functions for use in controllers
    return ({
      isLoggedIn: isLoggedIn,
      login: login,
      logout: logout,
      register: register,
      checkUser: checkUser,
      getUser: getUser
  });

  function getUser()
  {
    return user;
  }

  function isLoggedIn() {
    console.log('user: ' + user);
    var deferred = $q.defer();

    $http.get('/get_user_data')
      // handle success
      .success(function (data, status) {
        console.log(data);
        if(status === 200 && data.is_logged_in == true){
          user = data;
          deferred.resolve();
        } else if (status === 200) {
          user = null;
          deferred.resolve();
        }
      })
      .error(function (data) {
        user = false;
        deferred.reject();
      });
      // return promise object
      return deferred.promise;
  }

  function checkUser()
  {
    return user != null;
  }

  function login(username, password) {
  // create a new instance of deferred
    var deferred = $q.defer();

    $http.post('/login', {username: username, password: password})
      .success(function (data, status) {
        if(status === 200 && data.is_logged_in){
          user = data;
          deferred.resolve(user);
        } else if (status === 200) {
          user = null;
          deferred.reject("Invalid username and/or password.");
        }
      })
      .error(function (data) {
        user = null;
        deferred.reject("Unexpected Error");
      });
      return deferred.promise;
    }

    function logout() {
      var deferred = $q.defer();
      $http.get('/logout')
        .success(function (data) {
          user = false;
          deferred.resolve();
        })
        .error(function (data) {
          user = false;
          deferred.reject();
        });
      return deferred.promise;
    }

    function register(user_data) {
      var deferred = $q.defer();

      $http.post('/register', user_data)
        .success(function (data, status) {
          if(status === 200 && data.result){
            user = data;
            console.log(data);
            deferred.resolve(data);
          } else {
            deferred.reject(data);
          }
        })
        .error(function (data) {
          console.log(data);
          console.log('error');
          deferred.reject(data);
        });
      return deferred.promise;
    }
}]);

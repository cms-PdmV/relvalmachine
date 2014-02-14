

var relval = angular.module('relval',[
        'ngRoute',
        'relvalControllers'
    ]);

relval.config(function($logProvider){
  $logProvider.debugEnabled(true);
});

relval.config(['$routeProvider', function($routeProvider){
    $routeProvider
    .when('/', {
        templateUrl: 'static/partials/home.html',
        controller: 'HomeCtrl'
    })
    .otherwise({
        templateUrl: 'static/partials/404.html'
      })
    }]);

// Routes for new request creation
relval.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/new', {
        templateUrl: 'static/partials/new-request/main.html',
        controller: 'NewRequestMainCtrl'
    })
    .when('/new/from-scratch', {
        templateUrl: 'static/partials/new-request/create-req.html',
        controller: 'NewRequestCreateCtrl'
    })
    .when('/new/clone', {
        templateUrl: 'static/partials/new-request/clone-req.html',
        controller: 'NewRequestCloneCtrl'
    })

}]);
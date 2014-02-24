

var relval = angular.module('relval',[
        'ngRoute',
        'ngResource',
        'relvalControllers',
        'relvalDirectives',
        'relvalServices'
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

// routes for predefined blobs
relval.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/blobs',  {
        templateUrl: 'static/partials/predefined-blobs/blobs.html',
        controller: 'BlobsCtrl'
    })
    .when('/blobs/new', {
        templateUrl: 'static/partials/new-request/clone-req.html',
        controller: 'NewRequestCloneCtrl'
    })
}]);
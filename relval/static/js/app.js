

var relval = angular.module('relval',[
        'ngRoute',
        'ngResource',
        'ngAnimate',
        'ui.bootstrap',
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
        redirectTo: '/home'
    })
    .when('/home', {
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

// routes for steps
relval.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/steps/',  {
        templateUrl: 'static/partials/steps/index.html',
        controller: 'StepsCtrl'
    })
    .when('/steps/new',  {
        templateUrl: 'static/partials/steps/new.html',
        controller: 'NewStepCtrl'
    })
    .when('/steps/clone/:stepId',  {
        templateUrl: 'static/partials/steps/new.html',
        controller: 'CloneStepCtrl'
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
        templateUrl: 'static/partials/predefined-blobs/edit.html',
        controller: 'NewBlobCtrl'
    })
    .when('/blobs/edit/:blobId', {
        templateUrl: 'static/partials/predefined-blobs/edit.html',
        controller: 'EditBlobCtrl'
    })
    .when('/blobs/clone/:blobId', {
        templateUrl: 'static/partials/predefined-blobs/edit.html',
        controller: 'CloneBlobCtrl'
    })
}]);

// routes for admin
relval.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/admin/',  {
        redirectTo: '/admin/users'
    })
    .when('/admin/:entity',  {
        templateUrl: 'static/partials/admin/index.html',
        controller: 'AdminCtrl'
    })
}]);


// Added for ability to do back() in history
relval.run(function ($rootScope, $location) {

    var history = [];

    $rootScope.$on('$routeChangeSuccess', function() {
        history.push($location.$$path);
    });

    $rootScope.back = function () {
        var prevUrl = history.length > 1 ? history.splice(-2)[0] : "/";
        $location.path(prevUrl);
    };

});
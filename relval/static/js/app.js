

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

// Routes for requests
relval.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/requests/',  {
        templateUrl: 'static/partials/requests/index.html',
        controller: 'RequestsCtrl',
        reloadOnSearch: false
    })
    .when('/requests/new', {
        templateUrl: 'static/partials/requests/edit.html',
        controller: 'NewRequestCtrl',
        reloadOnSearch: false
    })
    .when('/requests/clone/:requestId', {
        templateUrl: 'static/partials/requests/edit.html',
        controller: 'CloneRequestCtrl',
        reloadOnSearch: false
    })
    .when('/requests/edit/:requestId', {
        templateUrl: 'static/partials/requests/edit.html',
        controller: 'EditRequestCtrl',
        reloadOnSearch: false
    })
}]);

// routes for steps
relval.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/steps/',  {
        templateUrl: 'static/partials/steps/index.html',
        controller: 'StepsCtrl',
        reloadOnSearch: false
    })
    .when('/steps/new',  {
        templateUrl: 'static/partials/steps/edit.html',
        controller: 'NewStepCtrl',
        reloadOnSearch: false
    })
    .when('/steps/edit/:stepId',  {
        templateUrl: 'static/partials/steps/edit.html',
        controller: 'EditStepCtrl',
        reloadOnSearch: false
    })
    .when('/steps/clone/:stepId',  {
        templateUrl: 'static/partials/steps/edit.html',
        controller: 'CloneStepCtrl',
        reloadOnSearch: false
    })
}]);

// routes for predefined blobs
relval.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/blobs',  {
        templateUrl: 'static/partials/predefined-blobs/blobs.html',
        controller: 'BlobsCtrl',
        reloadOnSearch: false
    })
    .when('/blobs/new', {
        templateUrl: 'static/partials/predefined-blobs/edit.html',
        controller: 'NewBlobCtrl',
        reloadOnSearch: false
    })
    .when('/blobs/edit/:blobId', {
        templateUrl: 'static/partials/predefined-blobs/edit.html',
        controller: 'EditBlobCtrl',
        reloadOnSearch: false
    })
    .when('/blobs/clone/:blobId', {
        templateUrl: 'static/partials/predefined-blobs/edit.html',
        controller: 'CloneBlobCtrl',
        reloadOnSearch: false
    })
}]);

// routes for batches
relval.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/batches',  {
        templateUrl: 'static/partials/batches/index.html',
        controller: 'BatchesCtrl'
    })
    .when('/batches/new', {
        templateUrl: 'static/partials/batches/edit.html',
        controller: 'NewBatchCtrl'
    })
    .when('/batches/clone/:batchId', {
        templateUrl: 'static/partials/batches/edit.html',
        controller: 'CloneBatchCtrl'
    })
    .when('/batches/edit/:batchId', {
        templateUrl: 'static/partials/batches/edit.html',
        controller: 'EditBatchCtrl'
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
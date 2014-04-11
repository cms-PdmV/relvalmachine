/**
 * Created by Zygimantas Gatelis on 3/12/14.
 */
// controller extends BaseBlobsViewPageController with additional actions like edit, remove and clone blob
function BaseBlobsController($scope, $location, $route, PredefinedBlobs, AlertsService, BlobsSearchService) {
    angular.extend(this, new BaseViewPageController(
            $scope,
            $location,
            $route,
            PredefinedBlobs,
            AlertsService,
            BlobsSearchService
        ));
    $scope.entity = "blobs";
}

relvalControllers.controller('BlobsCtrl', ['$scope', '$location', '$route', 'PredefinedBlobs', 'AlertsService', 'BlobsSearchService',
    function($scope, $location, $route, PredefinedBlobs, AlertsService, BlobsSearchService) {
        angular.extend(this, new BaseBlobsController(
            $scope,
            $location,
            $route,
            PredefinedBlobs,
            AlertsService,
            BlobsSearchService
        ));
    }
]);

function BaseBlobEditPageController($scope, $rootScope) {
    angular.extend(this, new BaseEditPageController($scope));
    $scope.currentItem = {};
    $scope.currentItem.parameters = [{
        "flag": "",
        "value": ""
    }];

    $scope.addParametersRow = function() {
        $scope.currentItem.parameters.push({
            "flag": "",
            "value": ""
        });
    };

    $scope.removeParametersRow = function(index) {
        $scope.currentItem.parameters.splice(index, 1);
    };

    $scope.discardStepCreation = function() {
        $rootScope.back();
    };
}

function BlobPreloadCtrl($scope, $routeParams, PredefinedBlobs) {
    // load blob data
    $scope.id = $routeParams.blobId;
    var blob = PredefinedBlobs.get({item_id: $scope.id}, function() {
        $scope.currentItem = {};
        $scope.currentItem.title = blob.title;
        $scope.currentItem.immutable = blob.immutable;
        $scope.currentItem.parameters = blob.parameters;

        if ($scope.actionName == "Update") {
            $scope.oldTitle = blob.title;
        }
    });
}

relvalControllers.controller('NewBlobCtrl', ['$scope', '$rootScope', 'PredefinedBlobs', 'AlertsService',
    function($scope, $rootScope, PredefinedBlobs, AlertsService) {
        angular.extend(this, new BaseBlobEditPageController($scope, $rootScope));
        $scope.actionName = "Save";

        $scope.submit = function() {
            $scope.preSubmit();
            var blob = new PredefinedBlobs({
                title: $scope.currentItem.title,
                immutable: $scope.currentItem.immutable,
                parameters: $scope.currentItem.parameters
            });

            if ($scope.mainForm.$valid) {
                // POST to create new blob
                blob.$save(function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to create new predefined blob."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in blob creation form and then try to submit again."});
            }
        };
    }
]);

relvalControllers.controller('EditBlobCtrl', ['$scope', '$routeParams', '$rootScope', 'PredefinedBlobs', 'AlertsService',
    function($scope, $routeParams, $rootScope, PredefinedBlobs, AlertsService) {
        angular.extend(this, new BaseBlobEditPageController($scope, $rootScope));
        angular.extend(this, new BlobPreloadCtrl($scope, $routeParams, PredefinedBlobs));

        $scope.actionName = "Update";
        $scope.submit = function() {
            $scope.preSubmit();
            var blob = new PredefinedBlobs({
                title: $scope.currentItem.title,
                immutable: $scope.currentItem.immutable,
                parameters: $scope.currentItem.parameters
            });

            if ($scope.mainForm.$valid) {
                // PUT to update blob
                blob.$update({item_id: $scope.id}, function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to update predefined blob."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in blob creation form and then try to submit again."});
            }

        };
    }]);

relvalControllers.controller('CloneBlobCtrl', ['$scope', '$routeParams', '$rootScope', 'PredefinedBlobs', 'AlertsService',
    function($scope, $routeParams, $rootScope, PredefinedBlobs, AlertsService) {
        angular.extend(this, new BaseBlobEditPageController($scope, $rootScope));
        angular.extend(this, new BlobPreloadCtrl($scope, $routeParams, PredefinedBlobs));
        $scope.actionName = "Clone";

        $scope.submit = function() {
            $scope.preSubmit();
            var blob = new PredefinedBlobs({
                title: $scope.currentItem.title,
                immutable: $scope.currentItem.immutable,
                parameters: $scope.currentItem.parameters
            });

            if ($scope.mainForm.$valid) {
                $scope.submited = true;
                // POST to create new blob
                blob.$save(function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to update predefined blob."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in blob creation form and then try to submit again."});
            }
        };
    }]);

relvalControllers.controller('ViewBlobCtrl', ['$scope', '$routeParams', '$rootScope', 'PredefinedBlobs',
    function($scope, $routeParams, $rootScope, PredefinedBlobs) {
        angular.extend(this, new BlobPreloadCtrl($scope, $routeParams, PredefinedBlobs));

        $scope.back = function() {
            window.history.back();
        };
    }]);

var BlobSelectModalCtrl = function($scope,  $location, $route, $modalInstance, PredefinedBlobs, AlertsService, BlobsSearchService) {
    angular.extend(this, new BaseViewPageController(
        $scope,
        $location,
        $route,
        PredefinedBlobs,
        AlertsService,
        BlobsSearchService
    ));

    $scope.selectBlob = function(index) {
        $scope.clearParameters();
        $modalInstance.close($scope.items[index]);
    }

    $scope.cancel = function() {
        $scope.clearParameters();
        $modalInstance.dismiss('cancel');
    }
};

var BlobViewDetailsCtrl = function($scope, $modalInstance, PredefinedBlobs, blobId) {
    var blob = PredefinedBlobs.get({item_id: blobId}, function() {
        $scope.blob = {};
        $scope.blob.title = blob.title;
        $scope.blob.immutable = blob.immutable;
        $scope.blob.parameters = blob.parameters;
    });

    $scope.back = function() {
        $modalInstance.dismiss('cancel');
    }
}
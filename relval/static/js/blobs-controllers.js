/**
 * Created by Zygimantas Gatelis on 3/12/14.
 */
// controller extends BaseBlobsViewPageController with additional actions like edit, remove and clone blob
function BaseBlobsController($scope, $location, PredefinedBlobs, AlertsService, BlobsSearchService) {
    angular.extend(this, new BaseViewPageController(
            $scope,
            $location,
            PredefinedBlobs,
            AlertsService,
            BlobsSearchService
        ));

    $scope.showEditControllers = function(index) {
        return !$scope.items[index].immutable; // if not immutable than show edit controllers
    }

    $scope.editBlob = function(index) {
        var id = $scope.items[index].id;
        $scope.clearParameters();
        $location.path("/blobs/edit/" + id);
    };

    $scope.deleteBlob = function(index) {
        bootbox.confirm("Do You really want to remove predefined blob " + $scope.items[index].title + " ?",
            function(removeApproved) {
                if (removeApproved) {
                    var id = $scope.items[index].id
                    // DELETE blob
                    PredefinedBlobs.delete({blob_id: id}, function() {
                        $scope.items.splice(index, 1);
                        AlertsService.addSuccess({msg: "Predefined blob deleted successfully!"});
                    }, function() {
                        AlertsService.addError({msg: "Server error. Failed to remove predefined blob"});
                    });
                }});
    };

    $scope.cloneBlob = function(index) {
        var id = $scope.items[index].id;
        $scope.clearParameters();
        $location.path("/blobs/clone/" + id);
    }
}

relvalControllers.controller('BlobsCtrl', ['$scope', '$location', 'PredefinedBlobs', 'AlertsService', 'BlobsSearchService',
    function($scope, $location, PredefinedBlobs, AlertsService, BlobsSearchService) {
        angular.extend(this, new BaseBlobsController(
            $scope,
            $location,
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

function BaseBlobEditPageControllerWithInitialLoad($scope, $rootScope, $routeParams, PredefinedBlobs) {
    angular.extend(this, new BaseBlobEditPageController($scope, $rootScope));

    // load blob data
    $scope.id = $routeParams.blobId;
    var blob = PredefinedBlobs.get({blob_id: $scope.id}, function() {
        $scope.currentItem = {};
        $scope.currentItem.title = blob.title;
        $scope.currentItem.immutable = blob.immutable;
        $scope.currentItem.parameters = blob.parameters;
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
                blob.$create(function() {
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
        angular.extend(this, new BaseBlobEditPageControllerWithInitialLoad(
            $scope, $rootScope, $routeParams, PredefinedBlobs));
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
                blob.$update({blob_id: $scope.id}, function() {
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
        angular.extend(this, new BaseBlobEditPageControllerWithInitialLoad(
            $scope, $rootScope, $routeParams, PredefinedBlobs));
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
                blob.$create(function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to update predefined blob."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in blob creation form and then try to submit again."});
            }

        };
    }]);

var BlobSelectModalCtrl = function($scope,  $location, $modalInstance, PredefinedBlobs, AlertsService, BlobsSearchService) {
    angular.extend(this, new BaseViewPageController(
        $scope,
        PredefinedBlobs,
        AlertsService,
        BlobsSearchService
    ));

    $scope.selectBlob = function(index) {
        $modalInstance.close($scope.items[index]);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    }
};

var BlobViewDetailsCtrl = function($scope, $modalInstance, PredefinedBlobs, blobId) {
    var blob = PredefinedBlobs.get({blob_id: blobId}, function() {
        $scope.blob = {};
        $scope.blob.title = blob.title;
        $scope.blob.immutable = blob.immutable;
        $scope.blob.parameters = blob.parameters;
    });

    $scope.back = function() {
        $modalInstance.dismiss('cancel');
    }
}
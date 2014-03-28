/**
 * Created by Zygimantas Gatelis on 3/12/14.
 */

var BaseStepCtrl = function($scope) {
    $scope.getType = function(index) {
        var type = $scope.items[index].type;
        if (type == "default") return "Default";
        if (type == "first_mc") return "First MC"
        if (type == "first_data") return "First Data"
    }
}

relvalControllers.controller('StepsCtrl', ['$scope', '$location', 'Steps', 'AlertsService', 'StepsSearchService',
    function($scope, $location, Steps, AlertsService, StepsSearchService) {
        angular.extend(this, new BaseViewPageController(
            $scope,
            $location,
            Steps,
            AlertsService,
            StepsSearchService
        ));
        angular.extend(this, new BaseStepCtrl($scope));

        $scope.entity = "steps";
}]);

var BaseStepReadOnlyViewCtrl = function($scope, $modal) {
    $scope.isActiveForm = function(type) {
        return type == $scope.currentItem.type;
    }

    $scope.showBlobDetails = function(index) {
        var modal = $modal.open({
            templateUrl: 'static/partials/modal/blob-details.html',
            controller: BlobViewDetailsCtrl,
            resolve: {
                blobId: function() {
                    return $scope.currentItem.blobs[index].id
                }
            }
        });
    };
};

var BaseStepEditPageCtrl = function($scope, $modal, $rootScope) {
    angular.extend(this, new BaseEditPageController($scope));
    angular.extend(this, new BaseStepReadOnlyViewCtrl($scope, $modal));

    $scope.showAdvancedDataStepParams = false;

    $scope.addParametersRow = function() {
        $scope.currentItem.parameters.push({
            "flag": "",
            "value": ""
        });
    };

    $scope.removeParametersRow = function(index) {
        $scope.currentItem.parameters.splice(index, 1);
    };

    $scope.removeBlob = function(index) {
        var title = $scope.currentItem.blobs[index].title;
        bootbox.confirm("Do You really want to remove blob " + title + " ?", function(removeApproved) {
            if (removeApproved) {
                $scope.currentItem.blobs.splice(index, 1);
                $scope.$apply();
            }
        });
    };

    $scope.addBlob = function() {
        var modal = $modal.open({
            templateUrl: 'static/partials/modal/select-blob.html',
            windowClass: 'blobs-select-dialog',
            controller: BlobSelectModalCtrl
        });
        modal.result.then(function(selected) {
            $scope.currentItem.blobs.push(selected);
        });
    };

    $scope.discard = function() {
        $rootScope.back();
    };
}

var StepPreloadCtrl = function($scope, $routeParams, Steps) {
    $scope.currentItem = {};

    // load blob data
    $scope.id = $routeParams.stepId;
    var step = Steps.get({item_id: $scope.id}, function() {
        $scope.currentItem.title = step.title;
        $scope.currentItem.immutable = step.immutable;
        $scope.currentItem.parameters = step.parameters;
        $scope.currentItem.blobs = step.blobs;
        $scope.currentItem.type = step.type;
        $scope.currentItem.dataStep = step.data_step;
    });
}

function constructStep(scope, Steps) {
    var step = new Steps({
        title: scope.currentItem.title,
        immutable: scope.currentItem.immutable,
        type: scope.currentItem.type
    });
    if (scope.currentItem.type != "first_data") { // parameters and blobs has default and first mc steps
        step.parameters = scope.currentItem.parameters;
        step.blobs = scope.currentItem.blobs;
    }
    if (scope.currentItem.type != "default") { // data_step fields has first mc and first data steps
        step.data_step = scope.currentItem.dataStep;
    }
    return step;
}

relvalControllers.controller('NewStepCtrl', ['$scope', '$modal', '$rootScope', 'AlertsService', 'Steps',
    function($scope, $modal, $rootScope, AlertsService, Steps) {
        angular.extend(this, new BaseStepEditPageCtrl($scope, $modal, $rootScope));

        // prepare
        $scope.actionName = "Save";
        $scope.currentItem = {};
        $scope.currentItem.parameters = [{
            "flag": "",
            "value": ""
        }];
        $scope.currentItem.blobs = [];
        $scope.currentItem.immutable = false;
        $scope.currentItem.type = "default";
        $scope.currentItem.title = "";
        $scope.currentItem.dataStep = {};

        $scope.submit = function() {
            $scope.preSubmit();
            var step = constructStep($scope, Steps);
            // POST to create step
            if ($scope.mainForm.$valid) {
                step.$save(function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to create step."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in step creation error and then try to submit again."});
            }
        }
    }]);

relvalControllers.controller('CloneStepCtrl', ['$scope', '$modal', '$rootScope', '$routeParams', 'Steps', 'AlertsService',
    function($scope, $modal, $rootScope, $routeParams, Steps, AlertsService) {
        angular.extend(this, new BaseStepEditPageCtrl($scope, $modal, $rootScope));
        angular.extend(this, new StepPreloadCtrl($scope, $routeParams, Steps));

        $scope.actionName = "Clone";

        $scope.submit = function() {
            $scope.preSubmit();
            var step = constructStep($scope, Steps);
            // POST to create step
            if ($scope.mainForm.$valid) {
                step.$save(function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to create step."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in step creation error and then try to submit again."});
            }
        }

}]);

relvalControllers.controller('EditStepCtrl', ['$scope', '$modal', '$rootScope', '$routeParams', 'Steps', 'AlertsService',
    function($scope, $modal, $rootScope, $routeParams, Steps, AlertsService) {
        angular.extend(this, new BaseStepEditPageCtrl($scope, $modal, $rootScope));
        angular.extend(this, new StepPreloadCtrl($scope, $routeParams, Steps));

        $scope.actionName = "Update";

        $scope.submit = function() {
            $scope.preSubmit();
            var step = constructStep($scope, Steps);
            // PUT to update step
            if ($scope.mainForm.$valid) {
                step.$update({item_id: $scope.id}, function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to update step."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in step creation error and then try to submit again."});
            }
        }
    }]);

relvalControllers.controller('ViewStepCtrl', ['$scope', '$routeParams', '$rootScope', '$modal', 'Steps',
    function($scope, $routeParams, $rootScope, $modal, Steps) {
        angular.extend(this, new BaseStepCtrl($scope));
        angular.extend(this, new BaseStepReadOnlyViewCtrl($scope, $modal));
        angular.extend(this, new StepPreloadCtrl($scope, $routeParams, Steps));

        $scope.back = function() {
            $rootScope.back();
        };
    }]);

var StepSelectModalCtrl = function($scope, $location, $modalInstance, Steps, AlertsService, StepsSearchService) {
    angular.extend(this, new BaseViewPageController(
        $scope,
        $location,
        Steps,
        AlertsService,
        StepsSearchService
    ));
    angular.extend(this, new BaseStepCtrl($scope));

    $scope.selectStep = function(index) {
        $scope.clearParameters();
        $modalInstance.close($scope.items[index]);
    }

    $scope.cancel = function() {
        $scope.clearParameters();
        $modalInstance.dismiss('cancel');
    }
};

var StepViewDetailsCtrl = function($scope, $modalInstance, Steps, stepId) {
    var step = Steps.get({item_id: stepId}, function() {
        $scope.step = step;
        $scope.step.blobs.forEach(function(item) {
            item.show = false;
        });
    });

    $scope.blobToggle = function(index) {
        $scope.step.blobs[index].show =  !$scope.step.blobs[index].show;
    };

    $scope.getBlobClass = function(index) {
        if ($scope.step.blobs[index].show) return "glyphicon-minus"
        else return "glyphicon-plus";
    }

    $scope.doShowBlob = function(index) {
        return $scope.step.blobs[index].show;
    }

    $scope.back = function() {
        $modalInstance.dismiss('cancel');
    }
}

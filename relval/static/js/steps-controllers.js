/**
 * Created by Zygimantas Gatelis on 3/12/14.
 */

relvalControllers.controller('StepsCtrl', ['$scope', '$location', 'Steps', 'AlertsService', 'StepsSearchService',
    function($scope, $location, Steps, AlertsService, StepsSearchService) {
        angular.extend(this, new BaseViewPageController(
            $scope,
            Steps,
            AlertsService,
            StepsSearchService
        ));

        $scope.getType = function(index) {
            var type = $scope.items[index].type;
            if (type == "default") return "Default";
            if (type == "first_mc") return "First MC"
            if (type == "first_data") return "First Data"
        }

        $scope.showEditControllers = function(index) {
            return !$scope.items[index].immutable
        }

        $scope.editBlob = function(index) {
            $location.path('/steps/edit/' + $scope.items[index].id)
        }

        $scope.cloneStep = function(index) {
            var id = $scope.items[index].id
            $location.path("/steps/clone/" + id);
        }
}]);

var BaseStepEditPageCtrl = function($scope, $modal, $rootScope) {
    $scope.showAdvancedDataStepParams = false;

    $scope.isActiveForm = function(type) {
        return type == $scope.currentStep.type;
    }

    $scope.addParametersRow = function() {
        $scope.currentStep.parameters.push({
            "flag": "",
            "value": ""
        });
    };

    $scope.removeParametersRow = function(index) {
        $scope.currentStep.parameters.splice(index, 1);
    };

    $scope.showBlobDetails = function(index) {
        var modal = $modal.open({
            templateUrl: 'static/partials/modal/blob-details.html',
            controller: BlobViewDetailsCtrl,
            resolve: {
                blobId: function() {
                    return $scope.currentStep.blobs[index].id
                }
            }
        });
    };

    $scope.removeBlob = function(index) {
        var title = $scope.currentStep.blobs[index].title;
        bootbox.confirm("Do You really want to remove blob " + title + " ?", function(removeApproved) {
            if (removeApproved) {
                $scope.currentStep.blobs.splice(index, 1);
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
            $scope.currentStep.blobs.push(selected);
        });
    };

    $scope.discard = function() {
        $rootScope.back();
    };
}

var BaseStepEditPageWithPreloadCtrl = function($scope, $modal, $rootScope, $routeParams, Steps) {
    $scope.currentStep = {};
    angular.extend(this, new BaseStepEditPageCtrl(
        $scope,
        $modal,
        $rootScope
    ));
    // load blob data
    $scope.id = $routeParams.stepId;
    var step = Steps.get({step_id: $scope.id}, function() {
        $scope.currentStep.title = step.title;
        $scope.currentStep.immutable = step.immutable;
        $scope.currentStep.parameters = step.parameters;
        $scope.currentStep.blobs = step.blobs;
        $scope.currentStep.type = step.type;
        $scope.currentStep.dataSet = step.data_set;
        $scope.currentStep.dataStep = step.data_step;
    });
}

function constructStep(scope, Steps) {
    var step = new Steps({
        title: scope.currentStep.title,
        immutable: scope.currentStep.immutable,
        type: scope.currentStep.type
    });
    if (scope.currentStep.type != "first_data") {
        step.parameters = scope.currentStep.parameters;
        step.blobs = scope.currentStep.blobs;
        step.data_set = scope.currentStep.dataSet;
    } else {
        step.data_step = scope.currentStep.dataStep;
    }
    return step;
}

relvalControllers.controller('NewStepCtrl', ['$scope', '$modal', '$rootScope', 'AlertsService', 'Steps',
    function($scope, $modal, $rootScope, AlertsService, Steps) {
        angular.extend(this, new BaseStepEditPageCtrl(
            $scope,
            $modal,
            $rootScope
        ));

        // prepare
        $scope.actionName = "Save";
        $scope.currentStep = {};
        $scope.currentStep.parameters = [{
            "flag": "",
            "value": ""
        }];
        $scope.currentStep.blobs = [];
        $scope.currentStep.immutable = false;
        $scope.currentStep.type = "default";
        $scope.currentStep.title = "";
        $scope.currentStep.dataSet = "";
        $scope.currentStep.dataStep = {};

        $scope.saveStep = function() {
            var step = constructStep($scope, Steps);
            // POST to create step
            if ($scope.stepForm.$valid) {
                step.$create(function() {
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
        angular.extend(this, new BaseStepEditPageWithPreloadCtrl(
            $scope, $modal, $rootScope, $routeParams, Steps));

        $scope.actionName = "Clone";

        $scope.saveStep = function() {
            var step = constructStep($scope, Steps);
            // POST to create step
            if ($scope.stepForm.$valid) {
                step.$create(function() {
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
        angular.extend(this, new BaseStepEditPageWithPreloadCtrl(
            $scope, $modal, $rootScope, $routeParams, Steps));

        $scope.actionName = "Update";

        $scope.saveStep = function() {
            var step = constructStep($scope, Steps);
            // PUT to update step
            if ($scope.stepForm.$valid) {
                step.$update({step_id: $scope.id}, function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to update step."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in step creation error and then try to submit again."});
            }
        }
    }]);

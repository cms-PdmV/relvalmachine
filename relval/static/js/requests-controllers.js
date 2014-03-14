/**
 * Created by Zygimantas Gatelis on 3/13/14.
 */

relvalControllers.controller('RequestsCtrl', ['$scope', '$location', 'Requests', 'AlertsService', 'RequestsSearchService',
    function($scope, $location, Requests, AlertsService, RequestsSearchService) {
        angular.extend(this, new BaseViewPageController(
            $scope,
            Requests,
            AlertsService,
            RequestsSearchService
        ));

        $scope.cloneStep = function(index) {
            var id = $scope.items[index].id
            $location.path("/requests/clone/" + id);
        }

        $scope.showEditControllers = function(index) {
            return !$scope.items[index].immutable
        }

        $scope.editRequest = function(index) {
            var id = $scope.items[index].id
            $location.path("/requests/edit/" + id);
        }

        $scope.deleteRequest = function(index) {
            //TODO
        }
}]);

var BaseRequestEditPageCtrl = function($scope, $modal, $rootScope) {
    $scope.addStep = function() {
        var modal = $modal.open({
            templateUrl: 'static/partials/modal/select-step.html',
            windowClass: 'blobs-select-dialog',
            controller: StepSelectModalCtrl
        });
        modal.result.then(function(selected) {
            $scope.currentItem.steps.push(selected);
        });
    };

    $scope.removeStep = function(index) {
        var label = $scope.currentItem.steps[index].label;
        bootbox.confirm("Do You really want to remove blob " + label + " ?", function(removeApproved) {
            if (removeApproved) {
                $scope.currentItem.steps.splice(index, 1);
                $scope.$apply();
            }
        });
    };

    $scope.showStepDetails = function(index) {
        var modal = $modal.open({
            templateUrl: 'static/partials/modal/step-details.html',
            controller: StepViewDetailsCtrl,
            resolve: {
                stepId: function() {
                    return $scope.currentItem.steps[index].id
                }
            }
        });
    }

    $scope.discard = function() {
        $rootScope.back();
    };
}

var constructRequest = function(scope, Requests) {
    console.log(scope.currentItem.type);
    var request = new Requests({
        label: scope.currentItem.label,
        description: scope.currentItem.description,
        immutable: scope.currentItem.immutable,
        type: scope.currentItem.type,
        cmssw_release: scope.currentItem.cmssw_release,
        run_the_matrix_conf: scope.currentItem.run_the_matrix_conf,
        events: scope.currentItem.events,
        priority: scope.currentItem.priority
    });
    var steps = [];
    scope.currentItem.steps.forEach(function(step){
        steps.push({id: step.id});
    })
    request.steps = steps;
    return request;
}

var saveRequest = function(scope, rootScope, Requests, AlertsService) {
    if (scope.requestForm.$valid) {
        var request = constructRequest(scope, Requests);
        request.$create(function() {
            rootScope.back();
        }, function() {
            AlertsService.addError({msg: "Server Error. Failed to save step."});
        });
    } else {
        AlertsService.addError({msg: "Error! Fix errors in step creation error and then try to submit again."});
    }
}


relvalControllers.controller('NewRequestCtrl', ['$scope', '$modal', '$rootScope', 'AlertsService', 'Requests',
    function($scope, $modal, $rootScope, AlertsService, Requests) {
        angular.extend(this, new BaseRequestEditPageCtrl(
            $scope,
            $modal,
            $rootScope
        ));

        // prepare
        $scope.actionName = "Save";
        $scope.currentItem = {};
        $scope.currentItem.steps = [];
        $scope.currentItem.cmssw_release = "";
        $scope.currentItem.run_the_matrix_conf = "";
        $scope.currentItem.immutable = false;
        $scope.currentItem.label = "";
        $scope.currentItem.description = "";
        $scope.currentItem.type = "MC";

        $scope.saveRequest = function() {
            saveRequest($scope, $rootScope, Requests, AlertsService);
        }

    }]);

var BaseRequestEditPageWithPreloadCtrl = function($scope, $modal, $rootScope, $routeParams, Requests) {
    $scope.currentItem = {};
    angular.extend(this, new BaseRequestEditPageCtrl(
            $scope,
            $modal,
            $rootScope
    ));
    // load request data
    $scope.id = $routeParams.requestId;
    var request = Requests.get({request_id: $scope.id}, function() {
        $scope.currentItem.label = request.label;
        $scope.currentItem.description = request.description;
        $scope.currentItem.immutable = request.immutable;
        $scope.currentItem.type = request.type;
        $scope.currentItem.priority = request.priority;
        $scope.currentItem.cmssw_release = request.cmssw_release;
        $scope.currentItem.run_the_matrix_conf = request.run_the_matrix_conf;
        $scope.currentItem.events = request.events;
        $scope.currentItem.steps = request.steps
    });
}

relvalControllers.controller('CloneRequestCtrl', ['$scope', '$modal', '$rootScope', '$routeParams', 'AlertsService', 'Requests',
    function($scope, $modal, $rootScope, $routeParams, AlertsService, Requests) {
        angular.extend(this, new BaseRequestEditPageWithPreloadCtrl(
            $scope,
            $modal,
            $rootScope,
            $routeParams,
            Requests
        ));

        $scope.actionName = "Clone";

        $scope.saveRequest = function() {
            saveRequest($scope, $rootScope, Requests, AlertsService);
        }
    }]);

relvalControllers.controller('EditRequestCtrl', ['$scope', '$modal', '$rootScope', '$routeParams', 'AlertsService', 'Requests',
    function($scope, $modal, $rootScope, $routeParams, AlertsService, Requests) {
        angular.extend(this, new BaseRequestEditPageWithPreloadCtrl(
            $scope,
            $modal,
            $rootScope,
            $routeParams,
            Requests
        ));
        $scope.actionName = "Update";

        $scope.saveRequest = function() {
            var request = constructRequest($scope, Requests);
            // PUT to update step
            if ($scope.requestForm.$valid) {
                request.$update({request_id: $scope.id}, function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to update request."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in request form and then try to submit again."});
            }
        }

    }]);
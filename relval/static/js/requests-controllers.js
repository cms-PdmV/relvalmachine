/**
 * Created by Zygimantas Gatelis on 3/13/14.
 */

relvalControllers.controller('RequestsCtrl', ['$scope', '$location', 'Requests', 'AlertsService', 'RequestsSearchService',
    function($scope, $location, Requests, AlertsService, RequestsSearchService) {
        angular.extend(this, new BaseViewPageController(
            $scope,
            $location,
            Requests,
            AlertsService,
            RequestsSearchService
        ));
        $scope.entity = "requests";

        $scope.cloneStep = function(index) {
            var id = $scope.items[index].id;
            $scope.clearParameters();
            $location.path("/requests/clone/" + id);
        };

        $scope.showEditControllers = function(index) {
            return !$scope.items[index].immutable
        };

        $scope.edit = function(index) {
            var id = $scope.items[index].id;
            $scope.clearParameters();
            $location.path("/requests/edit/" + id);
        };
}]);

var BaseRequestReadOnlyViewCtrl = function($scope, $modal) {
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
};


var BaseRequestEditPageCtrl = function($scope, $modal, $rootScope) {
    angular.extend(this, new BaseEditPageController($scope));
    angular.extend(this, new BaseRequestReadOnlyViewCtrl($scope, $modal));

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
        var title = $scope.currentItem.steps[index].title;
        bootbox.confirm("Do You really want to remove step " + title + " ?", function(removeApproved) {
            if (removeApproved) {
                $scope.currentItem.steps.splice(index, 1);
                $scope.$apply();
            }
        });
    };

    $scope.discard = function() {
        $rootScope.back();
    };
}

var constructRequest = function(scope, Requests) {
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
    scope.preSubmit();
    if (scope.mainForm.$valid) {
        var request = constructRequest(scope, Requests);
        request.$save(function() {
            rootScope.back();
        }, function() {
            AlertsService.addError({msg: "Server Error. Failed to save request."});
        });
    } else {
        AlertsService.addError({msg: "Error! Fix errors in request creation form and then try to submit again."});
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

        $scope.submit = function() {
            saveRequest($scope, $rootScope, Requests, AlertsService);
        }

    }]);

var RequestPreloadCtrl = function($scope, $routeParams, Requests) {
    $scope.currentItem = {};
    // load request data
    $scope.id = $routeParams.requestId;
    var request = Requests.get({item_id: $scope.id}, function() {
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
        angular.extend(this, new BaseRequestEditPageCtrl($scope, $modal, $rootScope));
        angular.extend(this, new RequestPreloadCtrl($scope, $routeParams, Requests));

        $scope.actionName = "Clone";

        $scope.submit = function() {
            saveRequest($scope, $rootScope, Requests, AlertsService);
        }
    }]);

relvalControllers.controller('EditRequestCtrl', ['$scope', '$modal', '$rootScope', '$routeParams', 'AlertsService', 'Requests',
    function($scope, $modal, $rootScope, $routeParams, AlertsService, Requests) {
        angular.extend(this, new BaseRequestEditPageCtrl($scope, $modal, $rootScope));
        angular.extend(this, new RequestPreloadCtrl($scope, $routeParams, Requests));

        $scope.actionName = "Update";

        $scope.submit = function() {
            $scope.preSubmit();
            var request = constructRequest($scope, Requests);
            // PUT to update step
            if ($scope.mainForm.$valid) {
                request.$update({item_id: $scope.id}, function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to update request."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in request form and then try to submit again."});
            }
        }
    }]);

relvalControllers.controller('ViewRequestCtrl', ['$scope', '$modal', '$rootScope', '$routeParams', 'Requests',
    function($scope, $modal, $rootScope, $routeParams, Requests) {
        angular.extend(this, new BaseRequestReadOnlyViewCtrl($scope, $modal));
        angular.extend(this, new RequestPreloadCtrl($scope, $routeParams, Requests));

        $scope.back = function() {
            $rootScope.back();
        };
    }]);

var RequestSelectModalCtrl = function($scope, $location, $modalInstance, Requests, AlertsService, RequestsSearchService) {
    angular.extend(this, new BaseViewPageController(
        $scope,
        $location,
        Requests,
        AlertsService,
        RequestsSearchService
    ));


    $scope.selectRequest = function(index) {
        $scope.clearParameters();
        $modalInstance.close($scope.items[index]);
    }

    $scope.cancel = function() {
        $scope.clearParameters();
        $modalInstance.dismiss('cancel');
    }
};

var RequestViewDetailsCtrl = function($scope, $modalInstance, Requests, Steps, requestId, $modal) {
    var request = Requests.get({item_id: requestId}, function() {
        $scope.request = request;
    });

    $scope.showStep = function(index) {
        var modal = $modal.open({
            templateUrl: 'static/partials/modal/step-details.html',
            controller: StepViewDetailsCtrl,
            resolve: {
                stepId: function() {
                    return $scope.request.steps[index].id
                }
            }
        });
    };

    $scope.back = function() {
        $modalInstance.dismiss('cancel');
    }
}
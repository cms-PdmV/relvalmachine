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
        run_the_matrix_conf: scope.currentItem.run_the_matrix_conf
    });
    var steps = [];
    scope.currentItem.steps.forEach(function(step){
        steps.push({id: step.id});
    })
    request.steps = steps;
    return request;
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

            if ($scope.requestForm.$valid) {
                var request = constructRequest($scope, Requests);
                request.$create(function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to create step."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in step creation error and then try to submit again."});
            }
        }
    }]);
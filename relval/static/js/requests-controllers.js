/**
 * Created by Zygimantas Gatelis on 3/13/14.
 */

relvalControllers.controller('RequestsCtrl', ['$scope', '$location', 'Requests', 'AlertsService', 'StepsSearchService',
    function($scope, $location, Requests, AlertsService, StepsSearchService) {
        angular.extend(this, new BaseViewPageController(
            $scope,
            Requests,
            AlertsService,
            StepsSearchService
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
        var title = $scope.currentItem.steps[index].title;
        bootbox.confirm("Do You really want to remove blob " + title + " ?", function(removeApproved) {
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
    var request = new Requests({
        title: scope.currentItem.title,
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
        $scope.currentItem.title = "";
        $scope.currentItem.description = "";
        $scope.currentItem.type = "";

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
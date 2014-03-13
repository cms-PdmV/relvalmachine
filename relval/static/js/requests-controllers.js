/**
 * Created by Zygimantas Gatelis on 3/13/14.
 */

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

    $scope.discard = function() {
        $rootScope.back();
    };
}

relvalControllers.controller('NewRequestCtrl', ['$scope', '$modal', '$rootScope', 'AlertsService', 'Steps',
    function($scope, $modal, $rootScope, AlertsService, Steps) {
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

            } else {
                AlertsService.addError({msg: "Error! Fix errors in step creation error and then try to submit again."});
            }
        }
    }]);
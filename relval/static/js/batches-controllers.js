/**
 * Created by Zygimantas Gatelis on 3/17/14.
 */
relvalControllers.controller('BatchesCtrl', ['$scope', '$location', 'Requests', 'AlertsService', 'RequestsSearchService',
    function ($scope, $location, Requests, AlertsService, RequestsSearchService) {
        angular.extend(this, new BaseViewPageController(
            $scope,
            Requests,
            AlertsService,
            RequestsSearchService
        ));
    }]);

var constructBatch = function(scope, Batches) {
    var batch = new Batches({
        title: scope.currentItem.title,
        description: scope.currentItem.description,
        immutable: scope.currentItem.immutable,
        run_the_matrix_conf: scope.currentItem.run_the_matrix_conf,
        priority: scope.currentItem.priority
    });
    var requests = [];
    scope.currentItem.requests.forEach(function(request){
        requests.push({id: request.id});
    })
    batch.requests = requests;
    return batch;
}

var BaseBatchEditPageCtrl = function($scope, $modal, $rootScope) {
    $scope.addRequest = function() {
        var modal = $modal.open({
            templateUrl: 'static/partials/modal/select-request.html',
            windowClass: 'blobs-select-dialog',
            controller: RequestSelectModalCtrl
        });
        modal.result.then(function(selected) {
            $scope.currentItem.requests.push(selected);
        });
    };

    $scope.removeRequest = function(index) {
        var label = $scope.currentItem.requests[index].label;
        bootbox.confirm("Do You really want to remove request " + label + " ?", function(removeApproved) {
            if (removeApproved) {
                $scope.currentItem.requests.splice(index, 1);
                $scope.$apply();
            }
        });
    };

    $scope.showRequestDetails = function(index) {
        // TODO
    }

    $scope.discard = function() {
        $rootScope.back();
    };
}

relvalControllers.controller('NewBatchCtrl', ['$scope', '$modal', '$rootScope', '$location', 'Batches', 'AlertsService',
    function($scope, $modal, $rootScope, $location, Batches, AlertsService) {
        angular.extend(this, new BaseBatchEditPageCtrl(
            $scope,
            $modal,
            $rootScope
        ));

        $scope.actionName = "Save";
        $scope.currentItem = {};
        $scope.currentItem.title = "";
        $scope.currentItem.description = "";
        $scope.currentItem.immutable = false;
        $scope.currentItem.requests = [];
        $scope.currentItem.run_the_matrix_conf = undefined;
        $scope.currentItem.priority = undefined;

        $scope.submit = function() {
            if ($scope.batchForm.$valid) {
                var batch = constructBatch($scope, Batches);
                batch.$save(function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to save batch."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in batch creation form and then try to submit again."});
            }
        }
    }]);

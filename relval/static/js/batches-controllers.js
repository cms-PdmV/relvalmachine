/**
 * Created by Zygimantas Gatelis on 3/17/14.
 */
relvalControllers.controller('BatchesCtrl', ['$scope', '$location', 'Batches', 'AlertsService', 'BatchesSearchService',
    function ($scope, $location, Batches, AlertsService, BatchesSearchService) {
        angular.extend(this, new BaseViewPageController(
            $scope,
            $location,
            Batches,
            AlertsService,
            BatchesSearchService
        ));
        $scope.entity = "batches";

        $scope.showEditControllers = function(index) {
            return !$scope.items[index].immutable;
        };

        $scope.clone = function(index) {
            var id = $scope.items[index].id;
            $scope.clearParameters();
            $location.path("/batches/clone/" + id);
        };

        $scope.edit = function(index) {
            var id = $scope.items[index].id;
            $scope.clearParameters();
            $location.path("/batches/edit/" + id);
        }

    }]);

var constructBatch = function(scope, Batches) {
    var batch = new Batches({
        title: scope.currentItem.title,
        description: scope.currentItem.description,
        immutable: scope.currentItem.immutable,
        run_the_matrix_conf: scope.currentItem.run_the_matrix_conf,
        cmssw_release: scope.currentItem.cmssw_release,
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
    angular.extend(this, new BaseEditPageController($scope));
    $scope.addRequest = function() {
        var modal = $modal.open({
            templateUrl: 'static/partials/modal/select-request.html',
            windowClass: 'wide-dialog',
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
        var modal = $modal.open({
            templateUrl: 'static/partials/modal/request-details.html',
            controller: RequestViewDetailsCtrl,
            resolve: {
                requestId: function() {
                    return $scope.currentItem.requests[index].id
                }
            }
        });
    }

    $scope.discard = function() {
        $rootScope.back();
    };
}

var BaseBatchEditWithPreloadCtrl = function($scope, $modal, $rootScope, $routeParams, Batches) {
    angular.extend(this, new BaseBatchEditPageCtrl(
        $scope,
        $modal,
        $rootScope
    ));
    $scope.currentItem = {};
    $scope.id = $routeParams.batchId;
    var batch = Batches.get({item_id: $scope.id}, function() {
        $scope.currentItem.title = batch.title;
        $scope.currentItem.immutable = batch.immutable;
        $scope.currentItem.description = batch.description;
        $scope.currentItem.run_the_matrix_conf = batch.run_the_matrix_conf;
        $scope.currentItem.cmssw_release = batch.cmssw_release;
        $scope.currentItem.requests = batch.requests;
        $scope.currentItem.priority = (batch.priority == 0) ? undefined : batch.priority;
    });
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
        $scope.currentItem.cmssw_release = undefined;

        $scope.submit = function() {
            $scope.preSubmit();
            if ($scope.mainForm.$valid) {
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

relvalControllers.controller('CloneBatchCtrl', ['$scope', '$modal', '$rootScope', '$location', '$routeParams', 'Batches', 'AlertsService',
    function($scope, $modal, $rootScope, $location, $routeParams, Batches, AlertsService) {
        angular.extend(this, new BaseBatchEditWithPreloadCtrl(
            $scope,
            $modal,
            $rootScope,
            $routeParams,
            Batches
        ));

        $scope.actionName = "Clone";
        $scope.submit = function() {
            $scope.preSubmit();
            if ($scope.mainForm.$valid) {
                var batch = constructBatch($scope, Batches);
                batch.$save({clone: true},function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to save batch."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in batch creation form and then try to submit again."});
            }
        }
    }]);

relvalControllers.controller('EditBatchCtrl', ['$scope', '$modal', '$rootScope', '$location', '$routeParams', 'Batches', 'AlertsService',
    function($scope, $modal, $rootScope, $location, $routeParams, Batches, AlertsService) {
        angular.extend(this, new BaseBatchEditWithPreloadCtrl(
            $scope,
            $modal,
            $rootScope,
            $routeParams,
            Batches
        ));

        $scope.actionName = "Update";
        $scope.submit = function() {
            $scope.preSubmit();
            if ($scope.mainForm.$valid) {
                var batch = constructBatch($scope, Batches);
                batch.$update({item_id: $scope.id}, function() {
                    $rootScope.back();
                }, function() {
                    AlertsService.addError({msg: "Server Error. Failed to update batch."});
                });
            } else {
                AlertsService.addError({msg: "Error! Fix errors in batch creation form and then try to submit again."});
            }
        }
    }]);

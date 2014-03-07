"use strict";

var relvalControllers = angular.module('relvalControllers', []);

relvalControllers.controller('HomeCtrl', ['$scope',
    function($scope) {
        $scope.test = "gavno"
    }
])

relvalControllers.controller('NavbarCtrl', ['$scope', '$location',
    function($scope, $location) {
        $scope.isActive = function(viewLocation) {
            return $location.path().lastIndexOf(viewLocation, 0) === 0
        };
    }
]);

relvalControllers.controller('AlertCtrl', ['$scope', 'AlertsService', function($scope, AlertsService) {
    $scope.alerts = AlertsService.fetchAlerts();

    $scope.closeAlert = function(index) {
        AlertsService.close(index);
    }
}]);

// New request creation controllers
relvalControllers.controller('NewRequestMainCtrl', ['$scope',
    function($scope) {
        console.log("log ")
    }
]);

relvalControllers.controller('NewRequestCreateCtrl', ['$scope',
    function($scope) {
        // in future check if there are available steps
        var stepId = 0;
        $scope.steps = [];
        $scope.currentStep = {};

        $scope.addStep = function() {
            $scope.showStepForm = true; // show step creation form

            $scope.currentStep.parameters = [{
                "flag": "",
                "value": ""
            }];
        };

        $scope.discardStepCreation = function() {
            $scope.showStepForm = false; // hide step creation form
        };

        $scope.saveStep = function() {
            $scope.showStepForm = false; // hide step creation form

            resolveSaveOrEditExisting();

            // clean up
            $scope.currentStep = {}
        };

        $scope.addParametersRow = function() {
            $scope.currentStep.parameters.push({
                "flag": "",
                "value": ""
            });
        };

        $scope.removeParametersRow = function(index) {
            $scope.currentStep.parameters.splice(index, 1);
        };

        $scope.editStep = function(index) {
            $scope.showStepForm = true; // show step creation form
            $scope.currentStep = $scope.steps[index];
        };

        $scope.removeStep = function(index) {
            var title = $scope.steps[index].title;
            var removeApproved = false;
            bootbox.confirm("Do You really want to remove step " + title + " ?", function(removeApproved) {
                if (removeApproved) {
                    // if current step is the one we are removing then clean it up
                    if ($scope.currentStep.hasOwnProperty('id')
                        && $scope.currentStep.id == $scope.steps[index].id) {

                        $scope.currentStep = {};
                        $scope.showStepForm = false;
                    }

                    $scope.steps.splice(index, 1);
                    $scope.$apply();
                }
            });
        }

        function stepIdPoll() {
            return stepId++;
        }

        // need to move somewhere else
        // pass parameters:
        //  ---->   $scope.steps - existing steps
        //  ---->   $scope.currentStep -> current one
        // maybe id poll function ??
        function resolveSaveOrEditExisting() {
            // if current step has id then we are editing existing one
            if ($scope.currentStep.hasOwnProperty('id')) {
                var i, indexToFind = -1;
                for (i = 0; i < $scope.steps.length; i++) {
                    if ($scope.steps[i].id == $scope.currentStep.id) {
                        indexToFind = i;
                        break;
                    }
                }
                $scope.steps[indexToFind] = $scope.currentStep;
                console.log("Existing id=" + $scope.currentStep.id);
            } else {
                $scope.steps.push({
                    'title': $scope.currentStep.title,
                    'parameters': $scope.currentStep.parameters,
                    'id': stepIdPoll()
                });
                console.log("New id=" + $scope.steps[$scope.steps.length-1].id);
            }
        }
    }
]);

relvalControllers.controller('NewRequestCloneCtrl', ['$scope',
    function($scope) {}
]);

// controllers related to blobs

// this controller provides basic functionality: search, pagination and sorting
function BaseBlobsViewPageController($scope, PredefinedBlobs, AlertsService, BlobsSearchService) {
    $scope.search = {
        searchText: ""
    };
    // pre-load blobs
    var resp = PredefinedBlobs.all(function() {
        $scope.totalItems = resp.total
        $scope.blobs = resp.blobs
    }, function() { // on failure
        AlertsService.addError({msg: "Server error. Failed to fetch predefined blobs"});
    });
    /*
     * Sorting
     */
    $scope.sort = {
        column: '',
        descending: false
    };

    $scope.changeSorting = function(column) {
        var sort = $scope.sort;

        if (sort.column == column) { // only change order
            sort.descending = !sort.descending;
        } else {
            sort.column = column;
            sort.descending = false;
        }
    };

    $scope.selectedCls = function(column) {
        // if column is the one that is selected then add class for icon
        return column == $scope.sort.column &&
            "fa fa-sort-alpha-" + ($scope.sort.descending ? "desc" : "asc")
    }

    /*
     * Pagination
     */
    $scope.itemsPerPage = 20;  // how many items are in one page
    $scope.currentPage = 1;    // current page that is selected
    $scope.maxSize = 10;       // how many pages display

    $scope.setPage = function(pageNo) {
        if (BlobsSearchService.isSearchingMode()) { // if in search mode then change page with same search query
            BlobsSearchService.changePage(pageNo, $scope.itemsPerPage, function(response) {
                $scope.totalItems = response.total;
                $scope.blobs = response.blobs;
            });
        } else {
            var resp = PredefinedBlobs.all({page_num: pageNo, items_per_page: $scope.itemsPerPage}, function() {
                $scope.totalItems = resp.total;
                $scope.blobs = resp.blobs;
            });
        }
        $scope.currentPage = pageNo;
    };

    /*
     * Search functionality
     */
    $scope.searchAll = function() {
        BlobsSearchService.search($scope.search.searchText, $scope.itemsPerPage, function(response) {
            $scope.totalItems = response.total
            $scope.blobs = response.blobs
            if ($scope.totalItems == 0) {
                AlertsService.addWarn({msg: "No result find for query " + $scope.search.searchText + "."})
            }
        });
    }

    $scope.resetSearch = function() {
        $scope.search.searchText = "";
        BlobsSearchService.resetSearch(function(response) {
            $scope.totalItems = response.total
            $scope.blobs = response.blobs
            $scope.currentPage = 1;
            $scope.sort.column = '';
        });
    }
}


// controller extends BaseBlobsViewPageController with additional actions like edit, remove and clone blob
function BaseBlobsController($scope, $location, PredefinedBlobs, AlertsService, BlobsSearchService) {
    angular.extend(this, new BaseBlobsViewPageController(
            $scope,
            PredefinedBlobs,
            AlertsService,
            BlobsSearchService
        ));

    $scope.showEditControllers = function(index) {
        return !$scope.blobs[index].immutable; // if not immutable than show edit controllers
    }

    $scope.editBlob = function(index) {
        var id = $scope.blobs[index].id
        $location.path("/blobs/edit/" + id);
    };

    $scope.deleteBlob = function(index) {
        bootbox.confirm("Do You really want to remove predefined blob " + $scope.blobs[index].title + " ?",
            function(removeApproved) {
                if (removeApproved) {
                    var id = $scope.blobs[index].id
                    // DELETE blob
                    PredefinedBlobs.delete({blob_id: id}, function() {
                        $scope.blobs.splice(index, 1);
                        AlertsService.addSuccess({msg: "Predefined blob deleted successfully!"});
                    }, function() {
                        AlertsService.addError({msg: "Server error. Failed to remove predefined blob"});
                    });
                }});
    };

    $scope.cloneBlob = function(index) {
        var id = $scope.blobs[index].id
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
    $scope.currentStep = {};
    $scope.currentStep.parameters = [{
        "flag": "",
        "value": ""
    }];

    $scope.addParametersRow = function() {
        $scope.currentStep.parameters.push({
            "flag": "",
            "value": ""
        });
    };

    $scope.removeParametersRow = function(index) {
        $scope.currentStep.parameters.splice(index, 1);
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
        $scope.currentStep = {};
        $scope.currentStep.title = blob.title;
        $scope.currentStep.immutable = blob.immutable;
        $scope.currentStep.parameters = blob.parameters;
    });
}

relvalControllers.controller('NewBlobCtrl', ['$scope', '$rootScope', 'PredefinedBlobs', 'AlertsService',
    function($scope, $rootScope, PredefinedBlobs, AlertsService) {
        angular.extend(this, new BaseBlobEditPageController($scope, $rootScope));
        $scope.actionName = "Save";

        $scope.saveStep = function() {
            var blob = new PredefinedBlobs({
                title: $scope.currentStep.title,
                immutable: $scope.currentStep.immutable,
                parameters: $scope.currentStep.parameters
            });

            // POST to create new blob
            blob.$create(function() {
                $rootScope.back();
            }, function() {
                AlertsService.addError("Server Error. Failed to create new predefined blob.");
            });
        };
    }
]);

relvalControllers.controller('EditBlobCtrl', ['$scope', '$routeParams', '$rootScope', 'PredefinedBlobs', 'AlertsService',
    function($scope, $routeParams, $rootScope, PredefinedBlobs, AlertsService) {
        angular.extend(this, new BaseBlobEditPageControllerWithInitialLoad(
            $scope, $rootScope, $routeParams, PredefinedBlobs));
        $scope.actionName = "Update";
        $scope.saveStep = function() {
            var blob = new PredefinedBlobs({
                title: $scope.currentStep.title,
                immutable: $scope.currentStep.immutable,
                parameters: $scope.currentStep.parameters
            });

            // POST to create new blob
            blob.$update({blob_id: $scope.id}, function() {
                $rootScope.back();
            }, function() {
                AlertsService.addError("Server Error. Failed to update predefined blob.");
            });
        };
    }]);

relvalControllers.controller('CloneBlobCtrl', ['$scope', '$routeParams', '$rootScope', 'PredefinedBlobs', 'AlertsService',
    function($scope, $routeParams, $rootScope, PredefinedBlobs, AlertsService) {
        angular.extend(this, new BaseBlobEditPageControllerWithInitialLoad(
            $scope, $rootScope, $routeParams, PredefinedBlobs));
        $scope.actionName = "Clone";

        $scope.saveStep = function() {
            var blob = new PredefinedBlobs({
                title: $scope.currentStep.title,
                immutable: $scope.currentStep.immutable,
                parameters: $scope.currentStep.parameters
            });

            // POST to create new blob
            blob.$create(function() {
                $rootScope.back();
            }, function() {
                AlertsService.addError("Server Error. Failed to update predefined blob.");
            });
        };
    }]);


// Steps controllers
relvalControllers.controller('StepsCtrl', ['$scope',
    function($scope) {
        // data fetch
    }]);

var BlobSelectModalCtrl = function($scope, $modalInstance, PredefinedBlobs, AlertsService, BlobsSearchService) {
    angular.extend(this, new BaseBlobsViewPageController(
        $scope,
        PredefinedBlobs,
        AlertsService,
        BlobsSearchService
    ));

    $scope.selectBlob = function(index) {
        $modalInstance.close($scope.blobs[index]);
    }

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    }
};

relvalControllers.controller('NewStepCtrl', ['$scope', '$modal', '$rootScope', 'AlertsService', 'Steps',
    function($scope, $modal, $rootScope, AlertsService, Steps) {
        // prepare
        $scope.actionName = "Save";
        $scope.currentStep = {};
        $scope.currentStep.parameters = [{
            "flag": "",
            "value": ""
        }];
        $scope.currentStep.blobs = [];
        $scope.currentStep.immutable = false;
        $scope.showMonteCarlo = true;
        $scope.currentStep.title = "";
        $scope.currentStep.dataSet = "";
        $scope.currentStep.runLumi = "";


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
            // TODO
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
        }

        $scope.saveStep = function() {
            var step = new Steps({
                title: $scope.currentStep.title,
                immutable: $scope.currentStep.immutable
            });
            if ($scope.showMonteCarlo) { // monte carlo step
                step.is_monte_carlo = true;
                step.parameters = $scope.currentStep.parameters;
                step.blobs = $scope.currentStep.blobs;
            } else {  // data step
                step.is_monte_carlo = false;
                step.data_set = $scope.currentStep.dataSet;
                step.run_lumi = $scope.currentStep.runLumi;
                console.log(step.data_set, step.run_lumi)
            }
            // POST to create step
            step.$create(function() {
                $rootScope.back();
            }, function() {
                AlertsService.addError({msg: "Server Error. Failed to create step."});
            });
        }
    }]);


// Admin controllers
relvalControllers.controller('AdminCtrl', ['$scope', '$routeParams',
    function($scope, $routeParams) {
        $scope.selectedTab = $routeParams.entity || 'users'; // set default user

        $scope.isActive = function(tab) {
            return $scope.selectedTab == tab;
        }

        $scope.selectTab = function(tab) {
            $scope.selectedTab = tab;
        }
    }]);

relvalControllers.controller('AdminUsersCtrl', ['$scope',
    function($scope) {

    }]);

relvalControllers.controller('AdminBlobsCtrl', ['$scope', '$location', 'PredefinedBlobs', 'AlertsService', 'BlobsSearchService',
    function($scope, $location, PredefinedBlobs, AlertsService, BlobsSearchService) {
        angular.extend(this, new BaseBlobsController(
            $scope,
            $location,
            PredefinedBlobs,
            AlertsService,
            BlobsSearchService
        ));
        $scope.showEditControllers = function(index) {
            return true; // always show edit controllers for admin
        }
    }]);

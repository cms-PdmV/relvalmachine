var relvalControllers = angular.module('relvalControllers', []);

relvalControllers.controller('HomeCtrl', ['$scope',
    function($scope) {
        $scope.test = "gavno"
    }
])

relvalControllers.controller('NavbarCtrl', ['$scope', '$location',
    function($scope, $location) {
        $scope.isActive = function(viewLocation) {
            return viewLocation === $location.path();
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
relvalControllers.controller('BlobsCtrl', ['$scope', '$location', 'PredefinedBlobs', 'AlertsService', 'BlobsSearchService',
    function($scope, $location, PredefinedBlobs, AlertsService, BlobsSearchService) {
        $scope.searchText = "";
        var resp = PredefinedBlobs.all(function() {
            $scope.totalItems = resp.total
            $scope.blobs = resp.blobs
        }, function() { // on failure
            AlertsService.addError({msg: "Server error. Failed to fetch predefined blobs"});
        });


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
                    $scope.totalItems = parseInt(resp.total);
                    $scope.blobs = resp.blobs;
                });
            }
            $scope.currentPage = pageNo;
        };

        /*
         * Search functionality
         */
        $scope.searchAll = function() {
            BlobsSearchService.search($scope.searchText, $scope.itemsPerPage, function(response) {
                $scope.totalItems = response.total
                $scope.blobs = response.blobs
                if ($scope.totalItems == 0) {
                    AlertsService.addWarn({msg: "No result find for query " + $scope.searchText + "."})
                }
            });
        }

        $scope.resetSearch = function() {
            $scope.searchText = "";
            BlobsSearchService.resetSearch(function(response) {
                $scope.totalItems = response.total
                $scope.blobs = response.blobs
                $scope.currentPage = 1;
                $scope.sort.column = '';
            });
        }

    }
]);

function BaseBlobEditPageController($scope, $location) {
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
        $location.path("/blobs");
    };
}

function BaseBlobEditPageControllerWithInitialLoad($scope, $location, $routeParams, PredefinedBlobs) {
    angular.extend(this, new BaseBlobEditPageController($scope, $location));

    // load blob data
    $scope.id = $routeParams.blobId;
    var blob = PredefinedBlobs.get({blob_id: $scope.id}, function() {
        $scope.currentStep = {};
        $scope.currentStep.title = blob.title;
        $scope.currentStep.immutable = blob.immutable;
        $scope.currentStep.parameters = blob.parameters;
    });
}

relvalControllers.controller('NewBlobCtrl', ['$scope', '$location', 'PredefinedBlobs',
    function($scope, $location, PredefinedBlobs) {
        angular.extend(this, new BaseBlobEditPageController($scope, $location));
        $scope.actionName = "Save";

        $scope.saveStep = function() {
            var blob = new PredefinedBlobs({
                title: $scope.currentStep.title,
                immutable: $scope.currentStep.immutable,
                parameters: $scope.currentStep.parameters
            });

            // POST to create new blob
            blob.$create(function() {
                $location.path("/blobs");
            });
        };
    }
]);

relvalControllers.controller('EditBlobCtrl', ['$scope', '$routeParams', '$location', 'PredefinedBlobs',
    function($scope, $routeParams, $location, PredefinedBlobs) {
        angular.extend(this, new BaseBlobEditPageControllerWithInitialLoad(
            $scope, $location, $routeParams, PredefinedBlobs));
        $scope.actionName = "Update";

        $scope.saveStep = function() {
            var blob = new PredefinedBlobs({
                title: $scope.currentStep.title,
                immutable: $scope.currentStep.immutable,
                parameters: $scope.currentStep.parameters
            });

            // POST to create new blob
            blob.$update({blob_id: $scope.id}, function() {
                $location.path("/blobs");
            });
        };
    }]);

relvalControllers.controller('CloneBlobCtrl', ['$scope', '$routeParams', '$location', 'PredefinedBlobs',
    function($scope, $routeParams, $location, PredefinedBlobs) {
        angular.extend(this, new BaseBlobEditPageControllerWithInitialLoad(
            $scope, $location, $routeParams, PredefinedBlobs));
        $scope.actionName = "Clone";

        $scope.saveStep = function() {
            var blob = new PredefinedBlobs({
                title: $scope.currentStep.title,
                immutable: $scope.currentStep.immutable,
                parameters: $scope.currentStep.parameters
            });

            // POST to create new blob
            blob.$create(function() {
                $location.path("/blobs");
            });
        };
    }]);
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
])

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
                "key": "",
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
                "key": "",
                "value": ""
            });
        };

        $scope.removeParametersRow = function(index) {
            $scope.currentStep.parameters.splice(index, 1);
        };

        $scope.editStep = function(index) {
            $scope.showStepForm = true; // show step creation form
            console.log(index)
            console.log($scope.steps[index]);
            $scope.currentStep = $scope.steps[index];
        };

        $scope.removeStep = function(index) {
            title = $scope.steps[index].title;
            removeApproved = false;
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
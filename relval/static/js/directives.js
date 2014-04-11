// directive for a single list

var relvalDirectives = angular.module('relvalDirectives', []);

relvalDirectives.directive('dragAndDropList', function() {

    return function(scope, element, attrs) {

        // variables used for dnd
        var toUpdate;
        var startIndex = -1;

        // watch the model, so we always know what element
        // is at a specific position
        scope.$watch(attrs.dragAndDropList, function(value) {
            toUpdate = value;
        },true);

        // use jquery to make the element sortable (dnd). This is called
        // when the element is rendered
        $(element[0]).sortable({
            items:'div.step',
            start:function (event, ui) {
                // on start we define where the item is dragged from
                startIndex = ($(ui.item).index());
            },
            stop:function (event, ui) {
                // on stop we determine the new index of the
                // item and store it there
                var newIndex = ($(ui.item).index());
                var toMove = toUpdate[startIndex];
                toUpdate.splice(startIndex, 1);
                toUpdate.splice(newIndex, 0, toMove);

                // we move items in the array, if we want
                // to trigger an update in angular use $apply()
                // since we're outside angulars lifecycle
                scope.$apply(scope.model);
            },
            axis:'y'
        })
    }
});

// workaround for angular chrome bug: https://github.com/angular/angular.js/issues/2144
// source: http://plnkr.co/edit/q0HmACwbyYMioat0oRSv?p=preview
relvalDirectives.directive('proxyValidity', function() {
    return {
      require: 'ngModel',
      link: function($scope, $element, $attrs, modelCtrl) {
        if (typeof $element.prop('validity') === 'undefined')
          return;

        $element.bind('input', function(e) {
          var validity = $element.prop('validity');
          $scope.$apply(function() {
            modelCtrl.$setValidity('badInput', !validity.badInput);
          });
        });
      }
    };
});

function AbstractValidationDirective($http, url, validity) {
    return {
        validateCall: function(ctrl, value) {
            if (!value) {
                ctrl.$setValidity(validity, false);
            } else {
                console.log(url);
                $http({
                    method: 'POST',
                    url: url,
                    data: {value: value}
                }).success(function(data) {
                    ctrl.$setValidity(validity, data.valid);

                }).error(function() {
                    ctrl.$setValidity(validity, false);
                })
            }
        },
        restrict: 'A',
        require: 'ngModel'
    }
}

// There should be a better way...
// Cannot avoid duplication cause seems like angular cashes method and
// if we create AbstractValidationDirective then same url will be called
// for different controllers until full page reload

relvalDirectives.directive('stepTitleValidation',['$http', function($http) {
    return {
        link:  function(scope, element, attrs, ctrl) {
            ctrl.$parsers.unshift(function(value) {
                if (!value) {
                    ctrl.$setValidity("unique", false);
                } else if (scope.oldTitle !== undefined && scope.oldTitle == value) {
                    ctrl.$setValidity("unique", true);
                } else {
                    $http({
                        method: 'POST',
                        url: "api/validate/step/title",
                        data: {value: value}
                    }).success(function(data) {
                            ctrl.$setValidity("unique", data.valid);

                        }).error(function() {
                            ctrl.$setValidity("unique", false);
                        })
                }
                return value;
            })
        },
        restrict: 'A',
        require: 'ngModel'
    }
}]);

relvalDirectives.directive('requestLabelValidation',['$http', function($http) {
    return {
        link:  function(scope, element, attrs, ctrl) {
            ctrl.$parsers.unshift(function(value) {
                if (!value) {
                    ctrl.$setValidity("unique", false);
                } else {
                    $http({
                        method: 'POST',
                        url: "api/validate/request/label",
                        data: {value: value}
                    }).success(function(data) {
                        ctrl.$setValidity("unique", data.valid);

                    }).error(function() {
                        ctrl.$setValidity("unique", false);
                    })
                }
                return value;
            })
        },
        restrict: 'A',
        require: 'ngModel'
    }
}]);

relvalDirectives.directive('blobTitleValidation',['$http', function($http) {
    return {
        link:  function(scope, element, attrs, ctrl) {
            ctrl.$parsers.unshift(function(value) {
                if (!value) {
                    ctrl.$setValidity("unique", false);
                } else {
                    $http({
                        method: 'POST',
                        url: "api/validate/blob/title",
                        data: {value: value}
                    }).success(function(data) {
                        ctrl.$setValidity("unique", data.valid);

                    }).error(function() {
                        ctrl.$setValidity("unique", false);
                    })
                }
                        return value;
                })
        },
        restrict: 'A',
        require: 'ngModel'
    }
}]);

relvalDirectives.directive('batchTitleValidation',['$http', function($http) {
    return {
        link:  function(scope, element, attrs, ctrl) {
            ctrl.$parsers.unshift(function(value) {
                if (!value) {
                    ctrl.$setValidity("unique", false);
                } else {
                    $http({
                        method: 'POST',
                        url: "api/validate/batch/title",
                        data: {value: value}
                    }).success(function(data) {
                        ctrl.$setValidity("unique", data.valid);

                    }).error(function() {
                        ctrl.$setValidity("unique", false);
                    })
                }
                        return value;
                })
        },
        restrict: 'A',
        require: 'ngModel'
    }
}]);

relvalDirectives.directive('entityActions', function() {
    return {
        templateUrl: "static/partials/reusable/entity-actions.html",
        restrict: "E"
    }
});
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
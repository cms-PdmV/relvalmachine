var relvalServices = angular.module('relvalServices', ['ngResource']);

relvalServices.factory('PredefinedBlobs', ['$resource', function($resource) {
        return $resource('api/predefined_blob/:blob_id', {}, {
            all: {
                method: 'GET'
            },
            search: {
                method: 'GET',
                isArray: true
            },
            get: {
                method: 'GET'
            },
            create: {
                method: 'POST'
            },
            delete: {
                method: 'DELETE'
            },
            update: {
                method: 'PUT'
            }
        });
}]);

relvalServices.factory('AlertsService', ['$timeout', function($timeout) {
        var alerts = [];
        var alertsService = {

            fetchAlerts: function() {
                console.log("Fetch");
                return alerts;
            },

            close: function(index) {
                alerts.splice(index, 1);
            },

            closeAfterDelay: function(alertToRemove) {
                $timeout(function() {
                    var index = alerts.indexOf(alertToRemove);
                    if (index > -1) {
                        alerts.splice(index, 1);
                    }
                }, 5000);
            },

            add: function(newAlert) {
                alerts.push(newAlert);
                this.closeAfterDelay(newAlert);
            },

            addSuccess:  function(newAlert) {
                newAlert.type = 'success';
                this.add(newAlert);
            },

            addError:  function(newAlert) {
                newAlert.type = 'danger';
                this.add(newAlert);
            }
        };


        return alertsService ;
}]);

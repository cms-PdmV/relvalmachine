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

relvalServices.factory('Steps', ['$resource', function($resource) {
        return $resource('api/steps/:step_id', {}, {
            all: {
                method: 'GET'
            },
            create: {
                method: 'POST'
            },
            get: {
                method: 'GET'
            }

        });
}]);

relvalServices.factory('AlertsService', ['$timeout', function($timeout) {
        var alerts = [];
        var time_out = 5000;
        var alertsService = {

            fetchAlerts: function() {
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
                }, time_out);
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
            },

            addWarn: function(newAlert) {
                newAlert.type = 'warning';
                this.add(newAlert)
            },

            setTimeout: function(time) {
                time_out = time;
            }
        };


        return alertsService ;
}]);


// abstract search service
var AbstractSearchService = function(resource) {
    var searchingMode = false;
    var query = "";

    var searchService = {

        search: function(search_query, items_per_page, callback) {
            searchingMode = true;
            var resp = resource.all({search: search_query, page_num: 1, items_per_page: items_per_page}, function() {
                callback(resp);
            });
            return resp;
        },

        changePage: function(page, itemsPerPage, callback) {
            var resp = resource.all({search: query, page_num: page, items_per_page: itemsPerPage},
                function() {
                    callback(resp)
                });
            return resp;
        },

        resetSearch: function(callback) {
            searchingMode = false;
            query = "";
            var resp = resource.all(function() {
                callback(resp)
            });
            return resp;
        },

        isSearchingMode: function() {
            return searchingMode;
        }
    };

    return searchService;
}


// blobs services
relvalServices.factory('BlobsSearchService', ['PredefinedBlobs', function(PredefinedBlobs) {
    var searchService = angular.extend(this, new AbstractSearchService(PredefinedBlobs));

    return searchService;
}]);

// steps services
relvalServices.factory('StepsSearchService', ['Steps', function(Steps) {
    var searchService = angular.extend(this, new AbstractSearchService(Steps));

    return searchService;
}]);

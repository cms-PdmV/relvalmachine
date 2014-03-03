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
            },

            addWarn: function(newAlert) {
                newAlert.type = 'warning';
                this.add(newAlert)
            }
        };


        return alertsService ;
}]);


// blobs services
relvalServices.factory('BlobsSearchService', ['PredefinedBlobs', function(PredefinedBlobs) {
    var searchingMode = false;
    var query = "";

    var searchService = {

        search: function(search_query, items_per_page, callback) {
            searchingMode = true;
            query = search_query;
            var resp = PredefinedBlobs.all({search: query, page_num: 1, items_per_page: items_per_page}, function() {
                callback(resp)
            });
            return resp;
        },

        changePage: function(page, itemsPerPage, callback) {
            var resp = PredefinedBlobs.all({search: query, page_num: page, items_per_page: itemsPerPage},
                function() {
                    callback(resp)
                });
            return resp;
        },

        resetSearch: function(callback) {
            searchingMode = false;
            query = "";
            var resp = PredefinedBlobs.all(function() {
                callback(resp)
            });
            return resp;
        },

        isSearchingMode: function() {
            return searchingMode;
        }
    };

    return searchService;
}]);

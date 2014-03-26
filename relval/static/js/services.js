var relvalServices = angular.module('relvalServices', ['ngResource']);

relvalServices.factory('PredefinedBlobs', ['$resource', function($resource) {
        return $resource('api/predefined_blob/:item_id', {}, {
            all: {
                method: 'GET'
            },
            update: {
                method: 'PUT'
            },
            details: {
                method: 'GET',
                url: 'api/predefined_blob/:item_id/details'
            }
            // Also available default methods: get, save, delete
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
            },
            update: {
                method: 'PUT'
            },
            details: {
                method: 'GET',
                url: 'api/steps/:item_id/details'
            }
        });
}]);

relvalServices.factory('Requests', ['$resource', function($resource) {
        return $resource('api/requests/:request_id', {}, {
            all: {
                method: 'GET'
            },
            create: {
                method: 'POST'
            },
            get: {
                method: 'GET'
            },
            update: {
                method: 'PUT'
            },
            details: {
                method: 'GET',
                url: 'api/requests/:item_id/details'
            }
        });
}]);

relvalServices.factory('Batches', ['$resource', function($resource) {
        return $resource('api/batches/:batch_id', {}, {
            all: {
                method: 'GET'
            },
            update: {
                method: 'PUT'
            }
        });
}]);

relvalServices.factory('Users', ['$resource', function($resource) {
        return $resource('api/users/:field', {}, {
            username: {
                method: 'GET',
                params: {field: 'username'}
            },
            email: {
                method: 'GET',
                params: {field: 'email'}
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

        search: function(search_query, items_per_page, page_num, callback) {
            searchingMode = true;
            query = search_query;
            var resp = resource.all({search: query, page_num: page_num, items_per_page: items_per_page}, function() {
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

        emptyQuery: function() {
            searchingMode = false;
            query = "";
        },

        isSearchingMode: function() {
            return searchingMode;
        },

        searchingModeOn: function(searchTerm) {
            searchingMode = true;
            query = searchTerm;
        }
    };

    return searchService;
}


// blobs services
relvalServices.factory('BlobsSearchService', ['PredefinedBlobs', '$location', function(PredefinedBlobs, $location) {
    var searchService = angular.extend(this, new AbstractSearchService(PredefinedBlobs));

    return searchService;
}]);

// steps services
relvalServices.factory('StepsSearchService', ['Steps', function(Steps) {
    var searchService = angular.extend(this, new AbstractSearchService(Steps));

    return searchService;
}]);

// requests services
relvalServices.factory('RequestsSearchService', ['Requests', function(Requests) {
    var searchService = angular.extend(this, new AbstractSearchService(Requests));

    return searchService;
}]);

// requests services
relvalServices.factory('BatchesSearchService', ['Batches', function(Batches) {
    var searchService = angular.extend(this, new AbstractSearchService(Batches));

    return searchService;
}]);

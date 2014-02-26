var relvalServices = angular.module('relvalServices', ['ngResource']);

relvalServices.factory('PredefinedBlobs', ['$resource', function($resource) {
        return $resource('api/predefined_blob/:blob_id', {}, {
            all: {
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
            }
        });
}]);
/**
 * Created by Zygimantas Gatelis on 3/3/14.
 */
"use strict";

describe('Blobs page', function() {

    //initialise module
    beforeEach(module('relvalControllers'));
    beforeEach(module('relvalServices'));

    describe('Blobs Controller:', function() {
        var scope, ctrl, $httpBackend, location, alertService, searchService;

        beforeEach(inject(function(_$httpBackend_, $rootScope, $location, $controller, BlobsSearchService) {
            $httpBackend = _$httpBackend_;
            scope = $rootScope.$new();
            location = $location;
            alertService = {};
            searchService = BlobsSearchService;
            scope.itemsPerPage = 3; // for easier pagination testing

            ctrl = $controller('BlobsCtrl', {
                $scope: scope,
                AlertsService: alertService,
                BlobsSearchService: searchService
            });
        }));

        afterEach(function() {
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
        });

        it('should call AlertService on failed response', function() {
            alertService.addError = jasmine.createSpy('addError');
            $httpBackend.when('GET', '/api/predefined_blob');
            $httpBackend.expectGET('api/predefined_blob').respond(500, '');
            $httpBackend.flush();
            expect(alertService.addError).toHaveBeenCalled();
        });



        describe('with initial blobs load', function() {
            var blobs;

            beforeEach(function() {
                blobs = []
                for (var i = 0; i < 3; i++) {
                    blobs.push({id: i, title: "title" + i})
                }
                $httpBackend.expectGET('api/predefined_blob').respond(200, {
                    total: 101,
                    blobs: blobs
                });
                $httpBackend.flush();
            });

            it('should fetch all predefined blobs', function() {
                expect(scope.blobs.length).toBe(3);
                expect(scope.totalItems).toBe(101);

            });

            it('should call server when changing page', function() {
                expect(scope.totalItems).toBe(101);

                scope.setPage(2);
                $httpBackend.expectGET('api/predefined_blob?items_per_page=100&page_num=2').respond(200, {
                    total: 102,
                    blobs: [blobs[2], blobs[3]]
                });
                $httpBackend.flush();

                expect(scope.totalItems).toBe(102);
                expect(scope.blobs).toEqual([blobs[2], blobs[3]])
            });

            it('should be able to search and paginate through search results', function() {
                // perform search
                scope.searchText = "text";
                scope.searchAll();

                $httpBackend.expectGET('api/predefined_blob?items_per_page=100&page_num=1&search=text').respond(200, {
                    total: 4,
                    blobs: [blobs[0], blobs[1]]
                });
                $httpBackend.flush();
                expect(scope.totalItems).toBe(4);
                expect(scope.blobs).toEqual([blobs[0], blobs[1]])
                expect(searchService.isSearchingMode()).toBe(true);

                // change page
                scope.setPage(2);
                $httpBackend.expectGET('api/predefined_blob?items_per_page=100&page_num=2&search=text').respond(200, {
                    total: 3,
                    blobs: [blobs[3]]
                });
                $httpBackend.flush();

                expect(scope.totalItems).toBe(3);
                expect(scope.blobs).toEqual([blobs[3]]);
                expect(searchService.isSearchingMode()).toBe(true);
            });

            it('should reset search when reset button pressed', function() {
                // perform search
                scope.searchText = "text";
                scope.searchAll();

                $httpBackend.expectGET('api/predefined_blob?items_per_page=100&page_num=1&search=text').respond(200, {
                    total: 4,
                    blobs: []
                });
                $httpBackend.flush();

                // reset
                scope.resetSearch();
                expect(scope.searchText).toBe('');
                expect(searchService.isSearchingMode()).toBe(false);
                $httpBackend.expectGET('api/predefined_blob').respond(200, {
                    total: 4,
                    blobs: [{id: 42}]
                });
                $httpBackend.flush();
            });
        });

        describe('with initial load', function() {

            beforeEach(function() {
                $httpBackend.expectGET('api/predefined_blob').respond(200, {
                    total: 1,
                    blobs: [{id: 42}]
                });
                $httpBackend.flush();
            });

            it('should redirect to edit page after edit', function() {
                scope.editBlob(0);
                expect(location.path()).toBe('/blobs/edit/42')
            });

            it('should send HTTP DELETE when confirm deletion and create success message', function() {
                alertService.addSuccess = jasmine.createSpy();

                scope.deleteBlob(0);

                // dialog should show up. Then press ok button
                waitsFor(function() {
                    return $(".modal-content").is(":visible");
                }, "Element did not show up", 1000);

                runs(function() {
                    $('.modal-dialog .modal-footer button[data-bb-handler="confirm"]').click();
                    $httpBackend.expectDELETE('api/predefined_blob/42').respond(200, '');
                    $httpBackend.flush();
                    expect(alertService.addSuccess).toHaveBeenCalled();
                });
            });

            it('should send HTTP DELETE and show error alert when deletion failed', function() {
                alertService.addError = jasmine.createSpy();

                scope.deleteBlob(0);

                // dialog should show up. Then press ok button
                waitsFor(function() {
                    return $(".modal-content").is(":visible");
                }, "Element did not show up", 1000);

                runs(function() {
                    $('.modal-dialog .modal-footer button[data-bb-handler="confirm"]').click();
                    $httpBackend.expectDELETE('api/predefined_blob/42').respond(500, '');
                    $httpBackend.flush();
                    expect(alertService.addError).toHaveBeenCalled();
                });
            });


            it('should send HTTP DELETE and show error alert when deletion failed', function() {
                alertService.addError = jasmine.createSpy();

                scope.deleteBlob(0);

                // dialog should show up. Then press ok button
                waitsFor(function() {
                    return $(".modal-content").is(":visible");
                }, "Element did not show up", 1000);

                runs(function() {
                    $('.modal-dialog .modal-footer button[data-bb-handler="cancel"]').click();
                });
            });

            it('should change sorting parameters on changeSorting()', function() {
                expect(scope.sort.descending).toBe(false);

                scope.changeSorting('title');
                expect(scope.sort.descending).toBe(false);
                expect(scope.sort.column).toBe('title');

                scope.changeSorting('title');
                expect(scope.sort.descending).toBe(true);
                expect(scope.sort.column).toBe('title');

                scope.changeSorting('creation_date');
                expect(scope.sort.descending).toBe(false);
                expect(scope.sort.column).toBe('creation_date');
            });
        });
    });
});
/**
 * Created by Zygimantas Gatelis on 3/12/14.
 */

// this controller provides basic functionality: search, pagination and sorting
function BaseViewPageController($scope, $location, Resource, AlertsService, SearchService) {
    $scope.search = {
        searchText: ""
    };
    SearchService.emptyQuery();

    var params = $location.search();

    $scope.maxSize = 10;       // how many pages display
    $scope.currentPage = params.page_num ? params.page_num : 1;   // current page in pagination
    $scope.itemsPerPage = params.items_per_page ? params.items_per_page : 20; // how many items to display in one page
    // DO NOT CHANGE THIS. This is hack to avoid double blobs GET call.
    // If total item is low number then page automatically set to 1 by angular-ui.pagination.
    $scope.totalItems = Number.POSITIVE_INFINITY;


    var populate = function(data) {
        $scope.totalItems = data.total;
        $scope.items = data.items;
        for (var i = 0; i < $scope.items.length; ++i) {
            $scope.items[i].index = i;
        }
    }

    /*
     * Pagination
     */
    $scope.setPage = function(pageNo) {
        if (SearchService.isSearchingMode()) { // if in search mode then change page with same search query
            SearchService.changePage(pageNo, $scope.itemsPerPage, function(response) {
                populate(response);
            });
        } else {
            var resp = Resource.all({page_num: pageNo, items_per_page: $scope.itemsPerPage}, function() {
                populate(resp);
            });
        }
        $scope.currentPage = pageNo;
        $location.search('page_num', pageNo);
    }

    // pre-load blobs
    if (params.search) {
        $scope.search.searchText = params.search;
        SearchService.searchingModeOn($scope.search.searchText);
        $scope.setPage($scope.currentPage);
    } else {
        $scope.setPage($scope.currentPage);
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
     * Search functionality
     */
    $scope.searchAll = function() {
        $location.search('search', $scope.search.searchText);
        $location.search('page_num', 1);
        $scope.currentPage = 1;
        SearchService.search($scope.search.searchText, $scope.itemsPerPage, $scope.currentPage,
            function(response) {
                populate(response);
                if ($scope.totalItems == 0) {
                    AlertsService.addWarn({msg: "No result find for query " + $scope.search.searchText + "."})
                }
            }
        );
    }

    $scope.resetSearch = function() {
        $scope.search.searchText = "";
        SearchService.resetSearch(function(response) {
            populate(response);
            $scope.currentPage = 1;
            $location.search("search", null);
            $location.search("page_num", 1);
            $scope.sort.column = '';
        });
    }

    $scope.delete = function(index) {
        bootbox.confirm("Do You really want to remove item " + $scope.items[index].title + " ?",
            function(removeApproved) {
                if (removeApproved) {
                    var id = $scope.items[index].id
                    // DELETE item
                    Resource.delete({item_id: id}, function() {
                        $scope.items.splice(index, 1);
                        AlertsService.addSuccess({msg: "Item deleted successfully!"});
                    }, function() {
                        AlertsService.addError({msg: "Server error. Failed to remove item"});
                    });
                }
            });
    };

    $scope.redirectToView = function(index) {
        var id = $scope.items[index].id;
        $scope.clearParameters();
        $location.path("/" + $scope.entity + "/view/" + id);
    }

    $scope.clearParameters = function() {
        $location.$$search = {};
        $location.url($location.path());
    }

    $scope.showDetails = function(index) {
        var resp = Resource.details({item_id: $scope.items[index].id}, function() {
            $scope.items[index].details = resp.details;
        });
        $scope.items[index].doShowDetails = true;
    }

    $scope.hideDetails = function(index) {
        $scope.items[index].doShowDetails = false;
    }
}

// this controller provides basic functionality for edit pages
function BaseEditPageController($scope) {
    $scope.submited = false;

    $scope.preSubmit = function() {
        $scope.submited = true;
        $scope.setFieldDirty($scope.mainForm.title);
    }

    $scope.setFieldDirty = function(field) {
        field.$setViewValue(field.$viewValue);
    }

    $scope.isTitleError = function() {
        return ($scope.mainForm.title.$dirty || $scope.submited) &&
                $scope.mainForm.title.$invalid;
    }

    $scope.isTitleEmpty = function() {
        return $scope.isTitleError() && $scope.mainForm.title.$error.required;
    }

    $scope.isTitleUnique = function() {
        return $scope.isTitleError() && $scope.mainForm.title.$error.unique;
    }
}

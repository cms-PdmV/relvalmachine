/**
 * Created by Zygimantas Gatelis on 3/12/14.
 */

// this controller provides basic functionality: search, pagination and sorting
function BaseViewPageController($scope, Resource, AlertsService, SearchService) {
    $scope.search = {
        searchText: ""
    };
    // pre-load blobs
    var resp = Resource.all(function() {
        $scope.totalItems = resp.total
        $scope.items = resp.items
    }, function() { // on failure
        AlertsService.addError({msg: "Server error. Failed to fetch data"});
    });

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
     * Pagination
     */
    $scope.itemsPerPage = 20;  // how many items are in one page
    $scope.currentPage = 1;    // current page that is selected
    $scope.maxSize = 10;       // how many pages display

    $scope.setPage = function(pageNo) {
        if (SearchService.isSearchingMode()) { // if in search mode then change page with same search query
            SearchService.changePage(pageNo, $scope.itemsPerPage, function(response) {
                $scope.totalItems = response.total;
                $scope.items = response.items;
            });
        } else {
            var resp = Resource.all({page_num: pageNo, items_per_page: $scope.itemsPerPage}, function() {
                $scope.totalItems = resp.total;
                $scope.items = resp.items;
            });
        }
        $scope.currentPage = pageNo;
    };

    /*
     * Search functionality
     */
    $scope.searchAll = function() {
        SearchService.search($scope.search.searchText, $scope.itemsPerPage, function(response) {
            $scope.totalItems = response.total
            $scope.items = response.items
            $scope.currentPage = 1;
            if ($scope.totalItems == 0) {
                AlertsService.addWarn({msg: "No result find for query " + $scope.search.searchText + "."})
            }
        });
    }

    $scope.resetSearch = function() {
        $scope.search.searchText = "";
        SearchService.resetSearch(function(response) {
            $scope.totalItems = response.total
            $scope.items = response.items
            $scope.currentPage = 1;
            $scope.sort.column = '';
        });
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

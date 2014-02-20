boulderDjangoApp.controller("meetupController", 
        ["$http", "$location", "$scope",
        function($http, $location, $scope){
    $scope.meetups = [];
    $scope.page = 1;
    $scope.count = 10;

    $scope.update = function() {
        var url = BASE_URL + '/meetups/?page=' + $scope.page 
            + '&count=' + $scope.count;
        $http.get(url).success(function(data) {
            $scope.meetups = data.meetups;
            $scope.page = data.page;
            $scope.count = data.count;
        }).error(function(data) {
            humane.log('Unable to load meetups!');
            $location.path('/');
        });
    };

    $scope.next = function() {
        $scope.page += 1;
        $scope.update();
    };

    $scope.previous = function() {
        if ($scope.page === 0) { return; }
        $scope.page -= 1;
        $scope.update();
    };

    $scope.update();
}]);

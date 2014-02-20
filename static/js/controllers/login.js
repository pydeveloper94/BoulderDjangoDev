boulderDjangoApp.controller("profileController",
        ["$cookies", "$http", "$location", "$routeParams", "$scope",
        function($cookies, $http, $location, $routeParams, $scope) {

    $scope.update = function() {
        // Loads a user
        if ($location.path().match(/\/profile\//)) {
            var user = $scope.user.username;
        }
        else {
            var user = $routeParams.username;
        }
        var url = BASE_URL + '/users/' + user + '/';
        $http.get(url).success(function(data) {
            $scope.company = data.company;
            $scope.email = data.email;
            $scope.interests = data.interests;
            $scope.jobTitle = data.job_title;
            $scope.username = data.username;
            $scope.website = data.website;
            if (!$location.path().match(/\/profile\/.+/)) {
                $scope.image = data.image;
            }
        }).error(function(data) {
            humane.log("Unable to load profile");
            $location.path('/');
        });
    };
    
    $scope.greeting = function() {
        if ($location.path() === '/profile/') {
            return 'Hello, ' + $scope.user.username + '!';
        }
        else {
            return 'Welcome to ' + $routeParams.username + '\'s profile!';
        }
    };
    
    $scope.isProfile = function() {
        return $location.path() === '/profile/';
    };
    
    $scope.viewImage = function(img) {
        var fileReader = new FileReader();
        fileReader.readAsDataURL(img);
        fileReader.onload = function() {
            $scope.image = fileReader.result;
            $scope.$digest();
        }
    };
    
    $scope.returnData = function() {
        var errors = [];
        if($scope.username === '') {
            errors.push('You cannot change your username to something blank.');
        }
        if (errors.length === 0) {
            var data = {"username": $scope.username};
            if ($scope.company) {
                data.company = $scope.company;
            }
            if ($scope.email) {
                data.email = $scope.email;
            }
            if ($scope.interests) {
                data.interests = $scope.interests;
            }
            if ($scope.jobTitle) {
                data.job_title = $scope.jobTitle;
            }
            if ($scope.website) {
                data.website = $scope.website;
            }
            if($scope.image) {
                data.image = $scope.image;
            }
            return data;
        }
    };

    $scope.save = function() {
        var data = $scope.returnData();
        var url = BASE_URL + '/users/' + $scope.user.username + '/';
        $http.put(url, data).success(function(data) {
            humane.log("Your profile was successfully saved!");
            //$scope.image = '';
            $scope.user.username = data.username;
            $scope.username = data.username;
            $cookies['username'] = data.username;
            $scope.company = data.company;
            $scope.email = data.email;
            $scope.interests = data.interests;
            $scope.jobTitle = data.job_title;
            $scope.website = data.website;
            // $location.path('/profile/');
        }).error(function(data) {
            humane.log(data.errors);
        });
    };

    $scope.update();
}]);

var boulderDjangoApp = angular.module('boulderDjangoApp',
    ['ngCookies', 'ngRoute', 'ngSanitize']);

var BASE_URL = 'http://localhost/api';

boulderDjangoApp.config(
        ["$httpProvider", "$routeProvider", 
        function($httpProvider, $routeProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    
    $routeProvider.
        when('/', {
            controller: 'indexController',
            templateUrl: 'views/home.html'
        }).
        when('/profile/', {
            controller: 'profileController',
            templateUrl: 'views/profile.html'
        }).
        when('/profile/edit/', {
            controller: 'profileController',
            templateUrl: 'views/profileEdit.html' 
        }).
        when('/profile/posts/', {
            controller: 'blogUserListController',
            templateUrl: 'views/blogList.html'
        }).
        when('/users/:username/', {
            controller: 'profileController',
            templateUrl: 'views/profile.html'
        }).
        when('/irc/', {
            templateUrl: 'views/irc.html'
        }).
        when('/blog/', {
            controller: 'blogListController',
            templateUrl: 'views/blogList.html'
        }).
        /* Blog routes */
        when('/blog/new/', {
            controller: 'blogEditController',
            templateUrl: 'views/blogEdit.html'
        }).
        when('/blog/:user/', {
            controller: 'blogUserListController',
            templateUrl: 'views/blogList.html',
        }).
        when('/blog/:user/:title/', {
            controller: 'blogDetailController',
            templateUrl: 'views/blogDetail.html'
        }).
        when('/blog/:user/:title/edit', {
            controller: 'blogEditController',
            templateUrl: 'views/blogEdit.html'
        }).
        /* Jobs routes */
        when('/jobs/', {
            controller: 'jobListController',
            templateUrl: 'views/jobList.html'
        }).
        when('/jobs/new/', {
            controller: 'jobEditController',
            templateUrl: 'views/jobEdit.html'
        }).
        when('/jobs/:company/', {
            controller: 'jobCompanyListController',
            templateUrl: 'views/jobList.html' 
        }).
        when('/jobs/:company/:pk/', {
            controller: 'jobDetailController',
            templateUrl: 'views/jobDetail.html'
        }).
        when('/jobs/:company/:pk/edit/', {
            controller: 'jobEditController',
            templateUrl: 'views/jobEdit.html'
        }).
        /* Meetup routes */
        when('/meetups/', {
            controller: 'meetupController',
            templateUrl: 'views/meetupList.html'
        }).
        otherwise({
            templateUrl: 'views/404.html',
        });
}]);

boulderDjangoApp.run(["$cookies", "$http", "$location", "$rootScope", 
        function($cookies, $http, $location, $rootScope) {
    $rootScope.isLoggedIn = false;
    $rootScope.loadUser = function() {
        // Function for loading a user into 
        if($rootScope.isLoggedIn) { 
            return $rootScope.user; 
        }
        
        // Load username from cookie
        if ($cookies.username) {
            $rootScope.user = {"username": $cookies.username};
            $rootScope.isLoggedIn = true;
        }
    };
    $rootScope.logout = function() {
        if($rootScope.isLoggedIn) {
            $rootScope.isLoggedIn = false;
            $rootScope.user = {};
            $http.get(BASE_URL + '/logout/').success(function() {
                $location.path("/");
                delete $cookies['sessionid'];
                delete $cookies['csrftoken'];
                delete $cookies['username'];
            });
        }
    }
    $rootScope.loadUser();
}]);

/* Angular navbarController */
boulderDjangoApp.controller("navbarController", ["$scope", "$location",
        function($scope, $location) {
    $scope.isActive = function(location) {
        return location === $location.path();
    };
}]);



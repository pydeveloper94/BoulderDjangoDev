boulderDjangoApp.controller('indexController', 
        ["$http", "$scope", 
        function($http, $scope) {
    var url = BASE_URL + '/home/';
    $http.get(url).success(function(data) {
        $scope.caption = data.caption;
        $scope.posts = data.posts;
        $scope.meetups = data.meetups;
        $scope.jobs = data.jobs;

        // Clean up post urls
        for (var post in $scope.posts) {
            post = $scope.posts[post];
            post.url = "#" + post.url.split(BASE_URL)[1];
        }

        // Clean up job urls
        for (var job in $scope.jobs) {
            job = $scope.jobs[job];
            job.url = "#" + job.url.split(BASE_URL)[1];
        }
    }).error(function(){
        $scope.caption = 'Boulder Django is a group for all levels';
    });
}]);

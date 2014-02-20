boulderDjangoApp.controller("jobListController",
        ["$http", "$scope",
        function($http, $scope) {
    $scope.jobs = [];
    $scope.page = 1;
    $scope.count = 10;

    $scope.update = function() {
        var url = BASE_URL + '/jobs/';
        $http.get(url).success(function(data) {
            $scope.page = data.page;
            $scope.count = data.count;
            $scope.jobs = data.jobs;
            for (var job in $scope.jobs) {
                // Fix urls
                job = $scope.jobs[job];
                job.company_url = "#" + job.company_url.split(BASE_URL)[1];
                job.url = "#" + '/jobs/' + job.company_slug + '/' + job.pk;
                job.user.url = "#" + job.user.url.split(BASE_URL)[1];
            }
            
        }).error(function(data) {
            humane.log('Error loading jobs');
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

boulderDjangoApp.controller('jobCompanyListController',
        ["$http", "$routeParams", "$scope",
        function($http, $routeParams, $scope) {
    $scope.jobs = [];
    $scope.page = 1;
    $scope.count = 10;

    $scope.update = function() {
        var url = BASE_URL + '/jobs/' + $routeParams.company + '/';
        $http.get(url).success(function(data) {
            $scope.page = data.page;
            $scope.count = data.count;
            $scope.jobs = data.jobs;
            for (var job in $scope.jobs) {
                // Fix urls
                job = $scope.jobs[job];
                job.url = "#" + job.company_slug + '/' + job.pk + '/';
            }
            
        }).error(function(data) {
            humane.log('Error loading jobs');
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

boulderDjangoApp.controller('jobDetailController',
        ["$http", "$location", "$routeParams", "$scope",
        function($http, $location, $routeParams, $scope) {
    var url = BASE_URL + '/jobs/' + $routeParams.pk + '/' 
    $scope.update = function() {
        $http.get(url).success(function(data) {
            $scope.job = data;
            $scope.username = data.username;
        }).error(function(data) {
            humane.log('This job does not exist');
        });
    };
    
    $scope.canEdit = function() {
        return ($scope.user.username === $scope.username);
    };
    
    $scope.edit = function() {
        var path = $location.path() + 'edit/';
        $location.path(path);
    };
    
    $scope.update();
}]);

boulderDjangoApp.controller('jobEditController',
        ["$http", "$location","$routeParams", "$scope", 
        function($http, $location, $routeParams, $scope) {
    $scope.job = {};
    if ($location.path() !== '/jobs/new/') {
        // Initializes data on the edit page
        var url = BASE_URL + '/jobs/' + $routeParams.pk + '/';
        $http.get(url).success(function(data) {
            $scope.job = data;
        }).error(function(data) {
            humane.log('This job does not exist or you are not authorized to ' 
                + 'edit it.');
            $location.path('/');
        });
    }
    
    $scope.renew = function() {
        var handler = StripeCheckout.configure({
            key: 'pk_test_KgTMz07gHk6sBZZorO9TDFat',
            image: 'http://www.mylittledjango.com/media/pony/ponyimage_image/16430.png',
            token: function(token, args) {
                var returnData = {"token": token.id}
                var url = BASE_URL + '/jobs/' + $routeParams.pk + '/renew/';
                $http.post(url, returnData).success(function(data) {
                    humane.log('Job successfully renewed.');
                }).error(function(data) {
                    humane.log('Your transaction failed.');
                });
            }
        });
        handler.open({
            name: 'Boulder Django',
            description: $scope.getDescription(),
            amount: 2500
        });
    };
    
    $scope.delete = function() {
        var url = BASE_URL + '/jobs/' + $routeParams.pk + '/';
        $http.delete(url).success(function(data) {
            humane.log('Job successfully deleted');
            $location.path('/');
        }).error(function(data) {
            humane.log('You cannnot delete this job');
        });
    };
    
    $scope.isEditing = function() {
        return ($location.path() !== '/jobs/new/');
    };
    
    $scope.returnData = function() {
        // Validates data before posting onto the server
        var errors = [];
        if (!$scope.token && $location.path() === '/jobs/new/') {
            errors.push('Please click on the credit card button and enter '
                + 'your information');
        }
        if (!$scope.job.title) {
            errors.push('You must include a title');
        }
        if (!$scope.job.company) {
            errors.push('You must include a company');
        }
        if (!$scope.job.description) {
            errors.push('You must include a description');
        }
        if (errors.length === 0) {
            var data = {
                'title': $scope.job.title,
                'company': $scope.job.company,
                'company_url': $scope.job.company_url,
                'description': $scope.job.description,
                'token': $scope.token,
            };
            return data;
        }
        else {
            humane.log(errors);
            return null;
        }
    };
    
    $scope._put = function(url, jsonData) {
        // PUTS a new job
        $http.put(url, jsonData).success(function(data) {
            humane.log('Save successful');
        }).error(function(data) {
            humane.log('Save unsuccessful');
        });
    };
    
    $scope._post = function(url, jsonData) {
        // POSTS a new job
        $http.post(url, jsonData).success(function(data) {
            humane.log('Job successfully posted');
            var path = '/jobs/' + data.company_slug + '/' + data.pk + '/edit/';
            $location.path(path);
        }).error(function(data) {
            humane.log('Error saving job');
        });
    };
    
    $scope.save = function() {
        // PUTS or POSTS data based on whether or not the current data is
        // being edited.
        var data = $scope.returnData();
        if (data === null) { return; }
        if ($location.path() !== '/jobs/new/') {
            var url = BASE_URL + '/jobs/' + $routeParams.pk + '/';
            $scope._put(url, data);
        }
        else {
            var url = BASE_URL + '/jobs/';
            $scope._post(url, data);
        }
    };
    
    $scope.getDescription = function() {
        // Returns a description for the stripe form
        if ($location.path() === '/jobs/new/') {
            return "Pay for a new job posting";
        }
        else {
            return "Add additional days to your job posting";
        }
    
    };
    
    $scope.raiseStripe = function() {
        var handler = StripeCheckout.configure({
            key: 'pk_test_KgTMz07gHk6sBZZorO9TDFat',
            image: 'http://www.mylittledjango.com/media/pony/ponyimage_image/16430.png',
            token: function(token, args) {
                $scope.token = token.id;
            }
        });
        handler.open({
            name: 'Boulder Django',
            description: $scope.getDescription(),
            amount: 2500
        });
    };
}]);

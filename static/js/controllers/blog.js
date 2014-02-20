boulderDjangoApp.controller('blogListController', 
        ["$http", "$scope", 
        function($http, $scope) {
    $scope.posts = {};
    $scope.page = 1;
    $scope.count = 10;
    
    $scope.update = function() {
        var url = BASE_URL + '/blog/?page=' + $scope.page + '&count='
            + $scope.count;
        $http.get(url).success(function(data) {
            $scope.posts = data.posts;
            $scope.page = data.page;
            $scope.count = data.count;
            for (var post in $scope.posts) {
                // Fix urls
                post = $scope.posts[post];
                post.url = "#" + post.url.split(BASE_URL)[1];
                post.user.url = "#" + post.user.url.split(BASE_URL)[1];
            }
        }).error(function(data) {
            humane.log('Error loading blog posts');
        });
    };

    $scope.next = function() {
        $scope.page += 1;
        $scope.update();
    };

    $scope.previous = function() {
        if ($scope.page === 1) { return; }
        $scope.page -= 1;
        $scope.update();
    };
    $scope.update();
}]);

boulderDjangoApp.controller('blogDetailController',
        ["$http", "$routeParams", "$scope",
        function($http, $routeParams, $scope) {
    var user = $routeParams.user;
    var title = $routeParams.title;
    var url = BASE_URL + '/blog/' + user + '/' + title + '/';

    $http.get(url).success(function(data) {
        $scope.post = data;
        $scope.post.user.url = "#" + data.user.url.split(BASE_URL)[1];
    }).error(function(data) {
        humane.log("This post does not exist");
        $location.path('/blog/');
    });

    $scope.canEdit = function() {
        // Used for showing/ hiding the edit button on a post.
        return ($scope.user.username === $routeParams.user);
    };

    $scope.edit = function() {
        // Returns the path to the edit page. Does not do any validation, use
        // with care.
        $location.path($location.path() + "edit/");
    };
}]);

boulderDjangoApp.controller('blogEditController',
        ["$http", "$location","$routeParams", "$scope", 
        function($http, $location, $routeParams, $scope) {
    $scope.pk = -1;
    
    if ($location.path() !== '/blog/new/') {
        // Initializes data on the edit page
        if (!$scope.canEdit()) {
            humane.log('You are not authorized to edit this post');
            $location.path('/blog/');
        }
        var user = $routeParams.user;
        var title = $routeParams.title;
        var url = BASE_URL + '/blog/' + user + '/' + title + '/';
        $http.get(url).success(function(data) {
            $scope.title = data.title;
            $scope.caption = data.caption;
            $scope.blogPost = data.text;
            $scope.pk = data.pk;
        }).error(function(data) {
            humane.log("This post does not exist.");
            $location.path('/blog/');
        });
    }

    $scope.canEdit = function() {
        // Used for showing/ hiding the edit button on a post.
        return ($scope.user.username === $routeParams.user);
    };

    $scope.editLink = function() {
        // Returns the path to the edit page. Does not do any validation, use
        // with care.
        return BASE_URL + $location.path() + "edit/";
    };

    $scope.returnData = function() {
        /* Function for composing blog post into an object. */
        var errors = [];
        if (!$scope.title) {
            errors.push('You must include a title.');
        }
        if (!$scope.caption) {
            errors.push('You must include a caption.');
        }
        if ($scope.title.length > 254) {
            errors.push('You title cannot be more than 254 characters')
        }
        if ($scope.caption.length > 500) {
            errors.push('Your caption cannot be more than 500 characters');
        }
        if (errors.length === 0) {
            var data = {
                'title': $scope.title,
                'caption': $scope.caption,
                'text': $scope.blogPost
            };
            if ($scope.pk !== -1) {
                data.pk = $scope.pk;
            }
            return data;
        }
        else {
            humane.log(errors);
            return null;
        }
    };

    $scope.deletePost = function(pk) {
        var user = $routeParams.user;
        var title = $routeParams.title;
        var url = BASE_URL + '/blog/' + user + '/' + title + '/';
        $http.delete(url).success(function() {
            humane.log("Post successfully deleted!");
            $location.path("/");
        }).error(function(data) {
            humane.log("Deletion failed.")
        });
    };
    
    $scope.isSaved = function() {
        // Checks if a post has been saved
        return !($scope.pk === -1);
    };
    
    $scope.saveFailed = function() {
        humane.log("You must fill all of the required fields before saving.");
    };
    
    $scope._oldSave = function(parameterData) {
        // Generic PUT save method for existing posts
        // Pass parameterData to decide whether or not it should be saved or
        // published.
        var user = $routeParams.user;
        var title = $routeParams.title;
        var url = BASE_URL + '/blog/' + user + '/' + title + '/';
        $http.put(url, parameterData).success(function(data) {
            humane.log("Save successful!");
        }).error(function(data) {
            humane.log(data.errors);
        });
        
    };

    $scope._newSave = function(parameterData) {
        // Generic POST save method for new blog posts
        var url = BASE_URL + '/blog/';
        $http.post(url, parameterData).success(function(data) {
            $scope.saveSuccessful();
            var url = data.url.split(BASE_URL)[1] + 'edit/';
            $location.path(url);
        }).error(function(data) {
            humane.log(data.errors);
        });
    };

    $scope._chooseSave = function(parameterData) {
        var returnData = $scope.returnData();
        if (!returnData) {return;} // Checks if the post is valid
        returnData.is_draft = parameterData.is_draft;
        if ($location.path() === '/blog/new/') {
            $scope._newSave(returnData);
        }
        else {
            $scope._oldSave(returnData);
        }
    };

    $scope.publish = function() {
        $scope._chooseSave({"is_draft": false});
    };

    $scope.save = function() {
        // Saves a draft for private viewing/editing
        $scope._chooseSave({"is_draft": true});
    };
}]);

boulderDjangoApp.controller('blogUserListController', 
        ["$http", "$location", "$routeParams", "$scope",
        function($http, $location, $routeParams, $scope) {
    $scope.page = 1;
    $scope.count = 10;
    
    $scope.update = function() {
        if ($location.path() === '/profile/posts/') {
            var url = BASE_URL + '/blog/' + $scope.user.username + '/';
        }
        else {
            var url = BASE_URL + '/blog/' + $routeParams.user + '/';
        }
        $http.get(url).success(function(data) {
            $scope.posts = data.posts;
            $scope.page = data.page;
            $scope.count = data.count;
            for (var post in $scope.posts) {
                post = $scope.posts[post];
                post.url = "#" + post.url.split(BASE_URL)[1];
                post.user.url = "#" + post.user.url.split(BASE_URL)[1];
            }
        }).error(function(data) {
            humane.log('Error loading posts')
            $location.path('/');
        }); 
    };
    
    $scope.next = function() {
        $scope.page += 1;
        $scope.update();
    };

    $scope.previous = function() {
        if ($scope.page === 1) { return; }
        $scope.page -= 1;
        $scope.update();
    };
    
    $scope.update();
}]);

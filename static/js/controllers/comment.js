boulderDjangoApp.controller('commentsController',
        ["$http", "$routeParams", "$scope",
        function($http, $routeParams, $scope) {
    // Comments attached to a blog post 
    $scope.comments = [];
    $scope.commentPage = 1;
    $scope.commentCount = 10;
    $scope.newCommentText = "";
    // Comment editing variables
    $scope.editCommentText = "";
    $scope.editCommentpk = -1;
    
    $scope.page = 1;
    $scope.count = 10;
    
    $scope.next = function() {
        $scope.page += 1;
        $scope.update();
    };
    
    $scope.previous = function() {
        if ($scope.page === 1) { return; }
        $scope.page -= 1;
        $scope.update();
    };
    
    $scope.update = function() {
        var url = BASE_URL + '/blog/' + $routeParams.user + '/'
            + $routeParams.title + '/comments/' + '?page=' + $scope.page 
            + '&count=' + $scope.count;
        $http.get(url).success(function(data) {
            $scope.comments = data.comments;
            $scope.page = data.page;
            $scope.count = data.count;
        }).error(function(data) {
            humane.log("Unable to load comments");
        });
    };
    
    $scope.edit = function(id) {
        // Launch a modal window with comment information.
        $scope.editCommentText = $scope.comments[id].text;
        $scope.editCommentpk = $scope.comments[id].pk;
        $('#commentEditDialog').modal('show');
    };
    
    $scope.submit = function() {
        // Creates a new comment and refreshes the
        if ($scope.newCommentText === '') {
            humane.log('You cannot sumbit a blank comment');
            return;
        }

        var parameterData = {
            "text": $scope.newCommentText
        };

        var url = BASE_URL + '/blog/' + $routeParams.user + '/'
            + $routeParams.title + '/comments/';
        $http.post(url, parameterData).success(function(data) {
            // Clear data and update
            $scope.newCommentText = '';
            $scope.update();
            humane.log('Comment submission successful');
        }).error(function(data) {
            humane.log('Comment submission failed');
        });
    };
    
    $scope.delete = function() {
        // Deletes a comment
        var url = BASE_URL + '/blog/' + $routeParams.user + '/'
            + $routeParams.title + '/comments/' + $scope.editCommentpk + '/';
        $http.delete(url).success(function(data) {
            $scope.update();
            humane.log('Comment successfully deleted');
        }).error(function(data) {
            humane.log('Comment deletion failed');
        });
        $('#commentEditDialog').modal('hide');
    };
    
    $scope.saveEdit = function() {
        // Saves a comment edit from the modal dialog.
        var parameterData = {
            "text": $scope.editCommentText,
        };
        var url = BASE_URL + '/blog/' + $routeParams.user + '/'
            + $routeParams.title + '/comments/' + $scope.editCommentpk + '/';
        $http.put(url, parameterData).success(function(data) {
            $scope.update();
            humane.log('Comment edit successful');
        }).error(function(data) {
            humane.log('Comment edit failed')
        });
        $('#commentEditDialog').modal('hide');
        $scope.editComment = "";
        $scope.editCommentpk = -1;
    };
    
    $scope.cancelEdit = function() {
        $('#commentEditDialog').modal('hide');
    };
    
    $scope.canEditComment = function(id) {
        return $scope.user.username ===  $scope.comments[id].user.username;
    };
    
    $scope.update();
}]);

boulderDjangoApp.directive('commentSection', [function() {
    return {
        restrict: 'E',
        controller: 'commentsController',
        templateUrl: 'views/commentSection.html'
    };
}]);

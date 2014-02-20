boulderDjangoApp.directive('markdown', [function() {
    var converter = new Showdown.converter();
    // Switch to marked + highlight.js
    return {
        restrict: 'E',
        link: function(scope, element, attrs, ctrl) {
            attrs.$observe('text', function(newValue) {
                element.html(converter.makeHtml(newValue));
            });
        }
    }
}]);

(function() {
  'use strict';
  angular.module('TPVpnapp',[
    'ngCookies'
  ], function($interpolateProvider){
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  })
  .config(['$httpProvider', function($httpProvider,$resourceProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    //$httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    //alert($('input[name=csrfmiddlewaretoken]').val());
    //$resourceProvider.defaults.stripTrailingSlashes = false;
  }])
  .run( function run($http, $cookies ){
    //$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    //$http.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
  })
  .directive('ngEnter', function() {
    return function(scope, element, attrs) {
      element.bind("keydown keypress", function(event) {
        if(event.which === 13) {
          scope.$apply(function(){
              scope.$eval(attrs.ngEnter, {'event': event});
          });

          event.preventDefault();
        }
      });
    };
  });
})();

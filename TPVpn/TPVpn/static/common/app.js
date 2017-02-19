//    --- License block --------------------------------------------------------
//    This file is part of TPVpn.
//
//    TPVpn is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    TPVpn is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with TPVpn.  If not, see <http://www.gnu.org/licenses/>.
//    --- End of License block -------------------------------------------------


(function() {
  'use strict';
  angular.module('TPVpnapp',[
    'ngCookies',
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
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
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

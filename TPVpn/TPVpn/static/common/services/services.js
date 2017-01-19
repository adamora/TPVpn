/*angular.module('TPVpnapp')

.service('RegisterService',
  function($http) {
    this.registerFor = function(dataObject) {
      $http({
        url: 'http://127.0.0.1/neWorker/',
        method: "POST",
        data: JSON.stringify(dataObject),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'}
      });
    }
});
*/
(function() {
  'use strict';
  angular.module('TPVpnapp')
  .service('RegisterService', function($http,$cookies,$location) {
    this.registerFor = function(dataObject,url) {
      var orig_url = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;
      return $http({
        url: orig_url + url,
        method: "POST",
        data: dataObject,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          //'X-CSRFToken': '{{ csrf_token }}'
        }
      });
    }
  });
})();

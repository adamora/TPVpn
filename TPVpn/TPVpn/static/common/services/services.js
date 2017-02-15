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

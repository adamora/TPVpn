/*angular.module('TPVpnapp')

.factory('UserNow',function(){
  return {
    data: {}
  };
});
*/
(function() {
  'use strict';
  angular.module('TPVpnapp')
  .factory('UserNow',function(){
    return {
      data: {}
    }
  })
  .factory('FactoriaPrueba', function() {
    return{
      data: 'algo mas'
    }
  });
})();

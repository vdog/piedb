/**
 * Created by Sandeep on 01/06/14.
 */

angular.module('movieApp.services',[]).factory('Movie',function($resource){
    return $resource('/orders/:id',{id:'@_id'},{
        update: {
            method: 'PUT'
        }
    });
}).factory('Customer', function($resource){
    return $resource('/customers/:id',{id:'@_id'},{
        update: {
          method: 'PUT'
        }
    });
//}).factory('Product', function($resource){
//     return $resource('/products
}).service('popupService',function($window){
    this.showPopup=function(message){
        return $window.confirm(message);
    }
});

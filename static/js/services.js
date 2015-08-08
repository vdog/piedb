/**
 * Created by Sandeep on 01/06/14.
 */

angular.module('orderApp.services',[]).factory('order',function($resource){
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
}).factory('Product', function($resource){
     return $resource('/products', {}, {});
}).factory('OrderDetail', function($resource){
        return $resource('/orderdetail', {},{

        });
}).factory('SubProducts', function($resource){
        return $resource('/subproducts/:id', {id: '@_id'},{
        });
}).service('popupService',function($window){
    this.showPopup=function(message){
        return $window.confirm(message);
    }
});

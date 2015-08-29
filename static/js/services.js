
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
     return $resource('/products/:id', {id:'@id'}, {});
}).factory('SubProduct', function($resource){
  return $resource('/subproducts/:id', {id:'@id'},{});
}).factory('OrderDetail', function($resource){
        return $resource('/orderdetail', {},{

        });
}).service('popupService',function($window){
    this.showPopup=function(message){
        return $window.confirm(message);
    }
});

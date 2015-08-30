/**
 * Created by Sandeep on 01/06/14.
 */
angular.module('orderApp.controllers',[]).controller('orderListController',function($scope,$state,$stateParams,popupService,$window,order){
    $scope.orderBy = $stateParams.orderBy;
    $scope.offset = 0;
    $scope.orders=order.query({orderBy:$stateParams.orderBy, offset:$scope.offset});

    $scope.nextPage = function(){
        $scope.offset += 10;
        $scope.orders=order.query({orderBy:$scope.orderBy, offset:$scope.offset});
    }

    $scope.prevPage = function() {
      if ($scope.offset >= 10){
          $scope.offset -= 10;
      }
      $scope.orders=order.query({orderBy:$scope.orderBy, offset:$scope.offset});
    }
    $scope.deleteorder=function(order){
        if(popupService.showPopup('Really delete this?')){
            order.$delete(function(){
                $window.location.href='';
            });
        }
    }
 }).controller('orderViewController',function($scope,$stateParams,order){

    $scope.order=order.get({id:$stateParams.id});

}).controller('orderCreateController',function($scope,$state,$stateParams,order){

    $scope.order=new order();

    $scope.addorder=function(){
        $scope.order.$save(function(){
            $state.go('orders');
        });
    }
}).controller('orderEditController',function($scope,$state,$stateParams,order, Customer, Product, OrderDetail, SubProduct){

    $scope.updateorder=function(){
        $scope.order.$update(function(){
            $state.go('orders');
        });
    };

    $scope.loadorder=function(){
        order.get({id:$stateParams.id}, function(data){
                $scope.order = data;
        });
      if ($stateParams.cID != null){
        Customer.query({search: $stateParams.cID, limit: 1}, function(data){
            $scope.order.customer = data[0];
            $scope.order.CustomerID = $scope.order.customer.CustomerID;
            console.log($scope.order.CustomerID);
            console.log(data);
        });

      }
        $( "#pickUpDate" ).datepicker({
          dateFormat: 'yy-mm-ddT00:00:00',
          onClose:function(){
            $scope.order.RequiredDate = this.value;
          }
        });
        console.log('loadorder');
    };

    $scope.queryChanged = function(){
      Customer.query({search: $scope.order.CustomerID, limit: 1}, function(data){
          $scope.order.customer = data[0];
          $scope.order.CustomerID = $scope.order.customer.CustomerID;
          console.log($scope.order.CustomerID);
          console.log(data);
      });
    }


    $scope.addDeet = function(){
            OrderDetail.get({}, function(data){
              $scope.order.details.push(data);
            });

    }

    $scope.updateProduct = function(product){
             SubProduct.query({productID: product.ProductID}, function(data){
              product.subproducts = data;
             })
    }

    Product.query({}, function(data){
            //console.log(data)
            $scope.products = data
            //console.log($scope.products)
    });

    SubProduct.query({}, function(data){
      $scope.subs = data
    });

    $scope.loadorder();

}).controller('OutlookListController',function($scope, $state, $stateParams, order){
    $scope.orders=order.query({startDate: '2014-10-09T00:00:00', endDate: '2014-10-17T00:00:00'});
}).controller('productListController',function($scope,Product){
  $scope.products = Product.query();
}).controller('productViewController',function($scope,$stateParams,Product){
  $scope.product = Product.get({id:$stateParams.id});
}).controller('CustomerLookupController',function($scope, $state, $stateParams, Customer){
    $scope.orders = Customer.query({search: $stateParams.search});
    $scope.offset = 0;
    $scope.queryChanged = function(){
      $scope.offset = 0;
      $scope.orders = Customer.query({search: $scope.search});
    }
    $scope.nextPage = function(){
        $scope.offset += 10;
        $scope.orders=Customer.query({search:$scope.search, offset:$scope.offset});
    }

    $scope.prevPage = function() {
      if ($scope.offset >= 10){
          $scope.offset -= 10;
      }
      $scope.orders=Customer.query({search:$scope.search, offset:$scope.offset});
    }
}).controller('CustomerViewController',function($scope, $state, $stateParams, Customer){
  $scope.customerID = $stateParams.id;
  console.log($scope.customerID);
  $scope.orders = Customer.query({id:$stateParams.id});
  $scope.offset = 0;
  $scope.nextPage = function(){
        $scope.offset += 10;
        $scope.orders=Customer.query({orderBy:$scope.orderBy, offset:$scope.offset});
    }

    $scope.prevPage = function() {
      if ($scope.offset >= 10){
          $scope.offset -= 10;
      }
      $scope.orders=Customer.query({orderBy:$scope.orderBy, offset:$scope.offset});
    }

}).controller('OrderReportsController',function($scope, $state, $stateParams, order){
    $scope.startDate = new Date().toISOString();
    $scope.endDate = new Date().toISOString();
    $( "#startDate" ).datepicker({
      dateFormat: 'yy-mm-ddT00:00:00',
      onClose:function(){
        $scope.startDate = this.value;
        $scope.orders = order.query({orderBy:$scope.orderBy, startDate:$scope.startDate, endDate:$scope.endDate});
      }
    });
    $( "#endDate" ).datepicker({
      dateFormat: 'yy-mm-ddT00:00:00',
      onClose:function(){
        $scope.endDate = this.value;
        $scope.orders = order.query({orderBy:$scope.orderBy, startDate:$scope.startDate, endDate:$scope.endDate});
      }
    });

});

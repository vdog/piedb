/**
 * Created by Sandeep on 01/06/14.
 */
angular.module('movieApp.controllers',[]).controller('MovieListController',function($scope,$state,$stateParams,popupService,$window,Movie){
    $scope.orderBy = $stateParams.orderBy;
    $scope.offset = 0;
    $scope.movies=Movie.query({orderBy:$stateParams.orderBy, offset:$scope.offset});

    $scope.nextPage = function(){
        $scope.offset += 10;
        $scope.movies=Movie.query({orderBy:$scope.orderBy, offset:$scope.offset});
    }

    $scope.prevPage = function() {
      if ($scope.offset >= 10){
          $scope.offset -= 10;
      }
      $scope.movies=Movie.query({orderBy:$scope.orderBy, offset:$scope.offset});
    }
    $scope.deleteMovie=function(movie){
        if(popupService.showPopup('Really delete this?')){
            movie.$delete(function(){
                $window.location.href='';
            });
        }
    }
 }).controller('MovieViewController',function($scope,$stateParams,Movie){

    $scope.movie=Movie.get({id:$stateParams.id});

}).controller('MovieCreateController',function($scope,$state,$stateParams,Movie){

    $scope.movie=new Movie();

    $scope.addMovie=function(){
        $scope.movie.$save(function(){
            $state.go('movies');
        });
    }
}).controller('MovieEditController',function($scope,$state,$stateParams,Movie, Customer, Product, SubProducts, OrderDetail){

    $scope.updateMovie=function(){
        $scope.movie.$update(function(){
            $state.go('movies');
        });
    };

    $scope.loadMovie=function(){
        Movie.get({id:$stateParams.id}, function(data){
                $scope.movie = data;
        });
    Product.query({}, function(data){
            console.log(data)
            $scope.products = data[0]
    });
        $( "#pickUpDate" ).datepicker({
          dateFormat: 'yy-mm-ddT00:00:00',
          onClose:function(){
            $scope.movie.RequiredDate = this.value;
          }
        });
        console.log('loadMovie');
    };

    $scope.queryChanged = function(){
      Customer.query({search: $scope.movie.CustomerID, limit: 1}, function(data){
          $scope.movie.customer = data[0];
          $scope.movie.CustomerID = $scope.movie.customer.CustomerID;
          console.log($scope.movie.CustomerID);
          console.log(data);
      });
    }

    $scope.addDeet = function(){
            OrderDetail.get({}, function(data){
              $scope.movie.details.push(data);
            });

    }

    $scope.loadMovie();

}).controller('OutlookListController',function($scope, $state, $stateParams, Movie){
    $scope.movies=Movie.query({startDate: '2014-10-09T00:00:00', endDate: '2014-10-17T00:00:00'});
}).controller('CustomerLookupController',function($scope, $state, $stateParams, Customer){
    $scope.movies = Customer.query({search: $stateParams.search});
    $scope.offset = 0;
    $scope.queryChanged = function(){
      $scope.offset = 0;
      $scope.movies = Customer.query({search: $scope.search});
    }
    $scope.nextPage = function(){
        $scope.offset += 10;
        $scope.movies=Customer.query({search:$scope.search, offset:$scope.offset});
    }

    $scope.prevPage = function() {
      if ($scope.offset >= 10){
          $scope.offset -= 10;
      }
      $scope.movies=Customer.query({search:$scope.search, offset:$scope.offset});
    }
}).controller('CustomerViewController',function($scope, $state, $stateParams, Customer){
  $scope.customerID = $stateParams.id;
  console.log($scope.customerID);
  $scope.movies = Customer.query({id:$stateParams.id});
  $scope.offset = 0;
  $scope.nextPage = function(){
        $scope.offset += 10;
        $scope.movies=Customer.query({orderBy:$scope.orderBy, offset:$scope.offset});
    }

    $scope.prevPage = function() {
      if ($scope.offset >= 10){
          $scope.offset -= 10;
      }
      $scope.movies=Customer.query({orderBy:$scope.orderBy, offset:$scope.offset});
    }

}).controller('OrderReportsController',function($scope, $state, $stateParams, Movie){
    $scope.startDate = new Date().toISOString();
    $scope.endDate = new Date().toISOString();
    $( "#startDate" ).datepicker({
      dateFormat: 'yy-mm-ddT00:00:00',
      onClose:function(){
        $scope.startDate = this.value;
        $scope.movies = Movie.query({orderBy:$scope.orderBy, startDate:$scope.startDate, endDate:$scope.endDate});
      }
    });
    $( "#endDate" ).datepicker({
      dateFormat: 'yy-mm-ddT00:00:00',
      onClose:function(){
        $scope.endDate = this.value;
        $scope.movies = Movie.query({orderBy:$scope.orderBy, startDate:$scope.startDate, endDate:$scope.endDate});
      }
    });

});

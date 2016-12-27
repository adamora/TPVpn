(function() {
  'use strict';
  angular.module('TPVpnapp')
  .controller('PruebaCTRL', function($scope,$cookies,PruebaService,FactoriaPrueba) {
    $scope.variable = {
      texto: PruebaService.inicio.texto,
    };
    $scope.algomas = FactoriaPrueba.data;
  })
  .controller('IndexCtrl',function($scope,RegisterService,UserNow,$window,$location){

    /*Variables globales de IndexCtrl*/
    //Mostrar partes de la plantilla cuando haya cliente
    $scope.showClient = false;
    $scope.actualClient = {
      image: "",
    };
    //Obtención de dinero
    $scope.moneyFromClient = 0;
    $scope.moneyFromWallet = 0;
    //Devolucion -> Para poner dos decimales redondeados
    $scope.devolution = 0;
    //Cantidades previas a seleccion de producto
    $scope.takeQuantity = 1;
    //IVAS
    $scope.ivaTot = 0;
    $scope.iva = {
      s: 0, //4% - superreducido
      r: 0, //10% - reducido
      g: 0  //21% - general
    };
    //Base Imponible
    $scope.baseImpTot = 0;
    $scope.baseImp = {
      s: 0, //4% - superreducido
      r: 0, //10% - reducido
      g: 0  //21% - general
    };
    //FILTROS
    var Provider = "";
    var Category = "";
    var Subcategory = "";
    //LISTAS PRODUCTOS
    $scope.completeList = []; //Lista completa de productos
    $scope.showProducts = []; //Lista de productos con filtros aplicados
    $scope.listProd = [];     //Lista de productos vendidos
    //LISTAS CLIENTES
    $scope.clientList = [];
    //IMPORTE TOTAL
    $scope.totalPrice = 0;
    /*Fin Variables globales*/


    /**
     * @ngdoc controller
     * @name TPVpnapp.controller:IndexCtrl
     * @element market
     * @function init
     *
     * @description
     * Take array of products and clients from backend when page loads
     *
     * **Note:**
     *
     * @example
       <my-directive ng-init='init(market)'></my-directive>
     */
    $scope.init = function(marketNow, worker) {
      var dataObject = jQuery.param({
        'status': 'done',
        'user': worker,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'operation': 'nothing',
        'market': marketNow
      });

      RegisterService.registerFor(dataObject,'/initial_data/')
        .success(function(response){
          $scope.completeList = response;
          $scope.showProducts = response;
        })
        .error(function(response){
          $window.alert('No conectado');
        })

      RegisterService.registerFor(dataObject,'/take_clients/')
        .success(function(response){
          $scope.clientList = response;
        })
        .error(function(response){
          $window.alert('No conectado clientes');
        })
    }


    $scope.takeProd = function(barCode) {
      if(barCode != "Vacio") {
        for(var i = 0; i<$scope.completeList.length; i++) {
          if($scope.completeList[i].barCode == barCode ) {
            var pk = $scope.completeList[i].id;
            var nameProd = $scope.completeList[i].name;
            var priceProd = $scope.completeList[i].sellPrice;
            $scope.addList(pk,nameProd,priceProd);
            $scope.takeBar=null;
          }
        }
      }
    }

    $scope.addList = function(pk,nameProd,priceProd){
      if(!angular.isNumber(priceProd)) {
        var aux = priceProd.split(',');
        var aux2 = '.';
        priceProd = aux[0].concat(aux2.concat(aux[1]));
      }


      if(parseFloat(priceProd) == 0.0) {
        return false;
      }
      if(nameProd == null || nameProd ==='' ) {
        return false;
      }

      var counter = 0;

      // && pk.indexOf('null')
      for (var i=0;i<$scope.listProd.length;i++){
        if ($scope.listProd[i].pk == pk || $scope.listProd[i].pk === pk){
          $scope.listProd[i].num = parseFloat($scope.listProd[i].num) + parseFloat($scope.takeQuantity);
          $scope.listProd[i].finalPrice = Math.round($scope.listProd[i].num * $scope.listProd[i].price * 100) / 100;
          counter++;
        }
      }
      if (counter == 0) {
        var obj = {
          pk:pk,
          num:$scope.takeQuantity,
          name:nameProd,
          price:parseFloat(priceProd),
          finalPrice:parseFloat(priceProd) * parseFloat($scope.takeQuantity)
        };

        $scope.listProd.push(obj);
      }

      //Comprobar cantidad > 0
      for (var i=0;i<$scope.listProd.length;i++) {
        if(parseFloat($scope.listProd[i].num) <= 0) {
          $scope.clearRowLP($scope.listProd[i].pk);
          i--;
        }
      }

      //Precio total 
      $scope.totalPrice = 0;
      for (var i=0;i<$scope.listProd.length;i++){
          $scope.totalPrice = Math.round(($scope.totalPrice + $scope.listProd[i].finalPrice)*100) / 100;
      }
      $scope.updateDevolution();

      //Resetear cantidad productos a añadir
      $scope.takeQuantity = 1;

      //Para mostrar BaseImp e IVA
      $scope.dataIvaMod();
      //FIN mostrar baseIMP e IVA

      //Baja el scroll
      var objDiv = document.getElementById("productListPanel");
      objDiv.scrollTop = objDiv.scrollHeight;
    }

    $scope.decreaseProdList = function(pk,name,sellPrice) {
      $scope.takeQuantity = -1;
      $scope.addList(pk,name,sellPrice);
    }

    $scope.clearRowLP = function(pk) {
      var counter = 0;
      var aux = [];
      if(angular.isNumber(parseInt(pk)) && !isNaN(parseInt(pk))){
        counter = 1;
      }
      for (var i=0;i<$scope.listProd.length;i++){
        if (counter == 1 && $scope.listProd[i].pk == pk){
          $scope.totalPrice = Math.round(($scope.totalPrice - $scope.listProd[i].finalPrice)*100)/100;
          $scope.devolution = Math.round(($scope.devolution + $scope.listProd[i].finalPrice)*100)/100;
        } else if (counter == 0 && $scope.listProd[i].pk === pk) {
          $scope.totalPrice = Math.round(($scope.totalPrice - $scope.listProd[i].finalPrice)*100)/100;
          $scope.devolution = Math.round(($scope.devolution + $scope.listProd[i].finalPrice)*100)/100;
        }
        else {
          aux.push($scope.listProd[i]);
        }
      }
      $scope.listProd = aux;
      $scope.dataIvaMod();
    }

    $scope.dataIvaMod = function() {
      $scope.baseImpTot = 0;
      $scope.ivaTot = 0;

      $scope.baseImp.g = 0;
      $scope.iva.g = 0;
      $scope.baseImp.r = 0;
      $scope.iva.r = 0;
      $scope.baseImp.s = 0;
      $scope.iva.s = 0;
      for(var i=0;i<$scope.completeList.length;i++) {
        for(var j=0;j<$scope.listProd.length;j++) {
          if($scope.completeList[i].id == $scope.listProd[j].pk){
            if ($scope.completeList[i].iva == 21) {
              var bI = ($scope.completeList[i].sellPrice/(1.21))*$scope.listProd[j].num;
              $scope.baseImp.g = Math.round(($scope.baseImp.g+bI)*100) / 100;
              $scope.iva.g = Math.round(($scope.iva.g +(bI * 0.21))*100) / 100;
            } else if ($scope.completeList[i].iva == 10) {
              var bI = ($scope.completeList[i].sellPrice/(1.10))*$scope.listProd[j].num;
              $scope.baseImp.r = Math.round(($scope.baseImp.r+bI)*100) / 100;
              $scope.iva.r = Math.round(($scope.iva.r +(bI * 0.1))*100) / 100;
            } else if ($scope.completeList[i].iva == 4) {
              var bI = ($scope.completeList[i].sellPrice/(1.04))*$scope.listProd[j].num;
              $scope.baseImp.s = Math.round(($scope.baseImp.s+bI)*100) / 100;
              $scope.iva.s = Math.round(($scope.iva.s +(bI * 0.04))*100) / 100;
            }
          }
        }
      }
      $scope.baseImpTot = Math.round(($scope.baseImp.g + $scope.baseImp.r + $scope.baseImp.s)*100)/100;
      $scope.ivaTot = Math.round(($scope.iva.g + $scope.iva.r + $scope.iva.s)*100)/100;
    }

    $scope.updateDevolution = function() {
      if($scope.moneyFromWallet === '')
        $scope.moneyFromWallet = 0;
      if($scope.moneyFromClient === '') {
        $scope.moneyFromClient = 0;
      }
      if($scope.moneyFromWallet > $scope.actualClient.wallet) {
        $scope.moneyFromWallet = $scope.actualClient.wallet;
      }
      if($scope.moneyFromWallet < 0) {
        $scope.moneyFromWallet = 0;
      }
      if($scope.moneyFromClient < 0) {
        $scope.moneyFromClient = 0;
      }
      var dev = parseFloat($scope.moneyFromClient) + parseFloat($scope.moneyFromWallet) - parseFloat($scope.totalPrice);
      $scope.devolution = Math.round(parseFloat(dev)*100) / 100;
    }


    /************* Funciones Cliente *************/
    $scope.addClient = function(dni) {
      for(var i=0;i<$scope.clientList.length;i++) {
        if ($scope.clientList[i].dni === dni) {
          $scope.actualClient = $scope.clientList[i];
          $scope.showClient = true;
        }
      }
    }

    $scope.clearClient = function() {
      $scope.showClient = false;
      $scope.moneyFromWallet = 0;
      $scope.updateDevolution();
      $scope.actualClient = "";
    }
    /************* Fin Funciones Cliente *************/

    /******** FILTRO PROVEEDOR ********/
    $scope.filterProvider = function(data) {
      Provider = data;
      if (Category === "" && Subcategory === "") {
        $scope.showProducts = $scope.completeList;
      }
      var aux = [];
      for(var i=0;i<$scope.showProducts.length;i++) {
        if($scope.showProducts[i].provider + "" === Provider) {
          aux.push($scope.showProducts[i]);
        }
      }
      $scope.showProducts = aux;
    }

    $scope.clearProvider = function() {
      $scope.showProducts = $scope.completeList;
      if (Category !== "" && Subcategory !== "") {
        $scope.filterCategory(Category);
        $scope.filterSubcategory(Subcategory);
      } else if (Category !== "") {
        $scope.filterCategory(Category);
      } else if (Subcategory !== "") {
        $scope.filterSubcategory(Subcategory);
      }
      Provider = "";
    }
    /******** FIN FILTRO PROVEEDOR ********/

    /******** FILTRO CATEGORÍA ********/
    $scope.filterCategory = function(data) {
      Category = data;
      if (Provider === "" && Subcategory === "") {
        $scope.showProducts = $scope.completeList;
      }
      var aux = [];
      for(var i=0;i<$scope.showProducts.length;i++) {
        if($scope.showProducts[i].category === Category) {
          aux.push($scope.showProducts[i]);
        }
      }
      $scope.showProducts = aux;
    }

    $scope.clearCategory = function() {
      $scope.showProducts = $scope.completeList;
      if (Provider !== "" && Subcategory !== "") {
        $scope.filterProvider(Provider);
        $scope.filterSubcategory(Subcategory);
      } else if (Provider !== "") {
        $scope.filterProvider(Provider);
      } else if (Subcategory !== "") {
        $scope.filterSubcategory(Subcategory);
      }
      Category = "";
    }
    /******** FIN FILTRO CATEGORÍA ********/

    /******** FILTRO SUBCATEGORÍA ********/
    $scope.filterSubcategory = function(data) {
      Subcategory = data;
      if (Provider === "" && Category === "") {
        $scope.showProducts = $scope.completeList;
      }
      var aux = [];
      for(var i=0;i<$scope.showProducts.length;i++) {
        if($scope.showProducts[i].subcategory === Subcategory) {
          aux.push($scope.showProducts[i]);
        }
      }
      $scope.showProducts = aux;
    }

    $scope.clearSubcategory = function() {
      $scope.showProducts = $scope.completeList;
      if (Provider !== "" && Category !== "") {
        $scope.filterProvider(Provider);
        $scope.filterCategory(Category);
      } else if (Provider !== "") {
        $scope.filterProvider(Provider);
      } else if (Subcategory !== "") {
        $scope.filterCategory(Category);
      }
      Subcategory = "";
    }
    /******** FIN FILTRO SUBCATEGORÍA ********/

    /**
     * @ngdoc controller
     * @name TPVpnapp.controller:IndexCtrl
     * @element market
     * @function updateServer
     *
     * @description
     * Load raw sell infromation to Server
     *
     * **Note:**
     *
     * @example
       <button ng-click='updateServer(market)'></my-directive>
     */
    $scope.updateServer = function(market,worker) {
      if($scope.listProd.length == 0) {
        alert("No se han seleccionado productos.");
        return false;
      }
      if($scope.devolution < 0) {
        alert("Importe insuficiente.");
        return false;
      }
      var dataObject = jQuery.param({
        'operation':'addSell',
        'market':market,
        'user':worker,
        'products':JSON.stringify($scope.listProd),
        'client':$scope.actualClient.dni,
        'usedWallet':$scope.moneyFromWallet,
        'clientMoney':$scope.moneyFromClient,
        'totalPrice':$scope.totalPrice,
        'devolution':$scope.devolution
      });

      RegisterService.registerFor(dataObject,'/addSell/')
       .success(function(response){
         //alert(response.location);
         $window.location.href = response.location;
       })
       .error(function(response){
         alert('No conectado. Fallo en venta.')
       })
    }

  })

  .controller('MovementsCtrl',function($scope,RegisterService,UserNow,$window,$location){
    //Lista ventas
    $scope.firstDate = '';
    /*$scope.listSales = [];
    $scope.listSalesAmount = [];
    $scope.listSalesDates = [];*/

    $scope.takeSales = function(marketPk,userPk) {
      var dataObject = jQuery.param({
        'operation':'takeSales',
        'user':userPk,
        'market':marketPk
      });

      RegisterService.registerFor(dataObject,'/takeSales/')
        .success(function(response){
          $scope.listSales = response;
          $scope.workOnListSale();
        })
        .error(function(response){
          alert("No conectado. Fallo al obtener ventas.");
        })
    }

    $scope.workOnListSale = function() {
      var aux = [];
      var dAux = [];
      var bAux = [];
      var str = '';
      var rawDate = '';
      var date = '';
      var counter=0;
      for(var i=0;i<$scope.listSales.length;i++) {
        str = $scope.listSales[i].date.split('T');
        rawDate = str[0].split('-');
        date = rawDate[2] + '-' + rawDate[1] + '-' + rawDate[0];
        if(i == 0){
          //PRIMERA FECHA PARA PLANTILLA
          $scope.firstDate = date;
          //FIN PRIMERA FECHA PARA PLANTILLA
          aux.push($scope.listSales[i].totAmount);
          bAux.push($scope.listSales[i].benefice);
          dAux.push(date);
        } else {
          counter = 0;
          for(var j=0;j<dAux.length;j++) {
            if(angular.equals(date,dAux[j])) {
              aux[j] = Math.round((parseFloat(aux[j]) + parseFloat($scope.listSales[i].totAmount))*100)/100;
              bAux[j] = Math.round((parseFloat(bAux[j]) + parseFloat($scope.listSales[i].benefice))*100)/100;
              counter = 1;
              break;
            }
          }
          if(counter == 0){
            aux.push($scope.listSales[i].totAmount);
            bAux.push($scope.listSales[i].benefice);
            dAux.push(date);
          }
        }
      }

      //$scope.listSalesAmount = aux;
      //$scope.listSalesDates = dAux;
      $window.listData = aux;
      $window.listDates = dAux;
      $window.listBenefice = bAux;
      return false;
    }
  });
})();

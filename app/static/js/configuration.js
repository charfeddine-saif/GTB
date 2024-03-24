








document.getElementById("ajoutbtn").addEventListener( "click", function(){
    var table = document.getElementsByTagName('table')[0];
    var popup = document.getElementsByClassName('popup')[0];
 
 
    if(table.style.display == 'none'){
     table.style.display = 'block';
     popup.style.display = 'none';
     window.location.reload()
    }else{
     table.style.display = 'none';
     popup.style.display = 'block';
    }
 
 
    }
 )







 document.getElementById("editbtn").addEventListener( "click", function(){

    console.log("object");
    // var table = document.getElementsByTagName('table')[0];
    // var popup = document.getElementsByClassName('popup1')[0];
 
 
    // if(table.style.display == 'none'){
    //  table.style.display = 'block';
    //  popup.style.display = 'none';
    //  window.location.reload()
    // }else{
    //  table.style.display = 'none';
    //  popup.style.display = 'block';
    // }
 
 
    }
 )







 document.getElementById("annulerbtn").addEventListener( "click", function(){
    var table = document.getElementsByTagName('table')[0];
    var popup = document.getElementsByClassName('popup')[0];
 
 
    if(table.style.display == 'none'){
     table.style.display = 'block';
     popup.style.display = 'none';
     window.location.reload()
    }else{
     table.style.display = 'none';
     popup.style.display = 'block';
    }
 
 
    }
 )


 document.getElementById("addbtn").addEventListener( "click", function(){

   var rowDiv = document.getElementById('row');

   var inputElement1 = document.createElement('input');
   var inputElement2 = document.createElement('input');
   inputElement1.setAttribute('type', 'text');
   inputElement1.setAttribute('placeholder', 'name');
   inputElement1.setAttribute('name', 'lampe');
   inputElement2.setAttribute('name', 'puissance');
   inputElement2.setAttribute('placeholder', 'puissance');
   inputElement2.setAttribute('type', 'text');
   inputElement1.classList.add('new-input');
   inputElement2.classList.add('new-input');
   inputElement2.style.width = "50px";
   inputElement1.style.width = "120px";
   inputElement1.style.marginLeft = "60px";
   inputElement2.style.marginLeft = "5px";


   
   rowDiv.appendChild(inputElement1);
   rowDiv.appendChild(inputElement2);


 }
 )

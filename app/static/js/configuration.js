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

        var inputElement = document.createElement('input');
        inputElement.setAttribute('type', 'text');
        inputElement.classList.add('lampinput');
        rowDiv.appendChild(inputElement);
 }
 )
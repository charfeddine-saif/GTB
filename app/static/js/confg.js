








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

    console.log("hey you clicked here");
    var trashBtn = '<span style="width: 50px; "><svg style="vertical-align: middle; cursor: pointer" width="20px" height="20px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg></span>';


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
   rowDiv.insertAdjacentHTML('beforeend', trashBtn);


 }
 )
 
    


 document.getElementById("addbtn2").addEventListener( "click", function(){

    console.log("hey you clicked here");
    var trashBtn = '<span style="width: 50px; "><svg style="vertical-align: middle; cursor: pointer" width="20px" height="20px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg></span>';


   var rowDiv = document.getElementById('row2');

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
   rowDiv.insertAdjacentHTML('beforeend', trashBtn);


 }
 )






 function openForm(button) {
   var row = button.parentNode.parentNode; // Get the parent row
   var nom_noeud = row.cells[0].innerText; // Get the value of the first cell
   var id_noeud = row.children[2].value; // Get the value of the first cell
   console.log("uuuuuu", id_noeud);
   var lampes_info = row.cells[1].querySelectorAll('.lampes span'); // Get lampes info
   var puissances = [];
   var rowDiv = document.getElementById('row2');
   console.log("row 0",row.cells[0]);
   console.log("row 1",row.cells[1]);
   console.log("row 2",row.cells[2]);
   console.log("row 0",row.children[2]);
   console.log("row",row);
   console.log("lampes",lampes_info);
   console.log("nom_noeud",nom_noeud);

   lampes_info.forEach(function(lampe,i) {
       if(i==0){
           document.getElementById("lampe1").value = lampe.innerText;
       }
       if(i==1){
           console.log("object");
           document.getElementById("puissance1").value = lampe.innerText.split(" ")[0];
       }
       if(i>1  && i % 2 == 0){

           var inputElement1 = document.createElement('input');
           inputElement1.setAttribute('type', 'text');
           inputElement1.setAttribute('placeholder', 'name');
           inputElement1.setAttribute('name', 'lampe');
           inputElement1.classList.add('new-input');
           inputElement1.style.width = "120px";
           inputElement1.style.marginLeft = "60px";
           inputElement1.value = lampe.innerText;
           rowDiv.appendChild(inputElement1);
       }
       if(i>1  && i % 2 != 0){

           var inputElement2 = document.createElement('input');
           inputElement2.setAttribute('placeholder', 'oooo');
           inputElement2.setAttribute('type', 'text');
           inputElement2.setAttribute('name', 'puissance');
           inputElement2.classList.add('new-input');   
           inputElement2.style.width = "50px";
           inputElement2.style.marginLeft = "5px";


           inputElement2.value = lampe.innerText.split(" ")[0];
           
           rowDiv.appendChild(inputElement2);
}
       // document.getElementsByClassName("new-input")[i] = lampe.innerText;
       // console.log("i",lampe.innerText);
   });
   var modal = document.querySelector('#popup1');
   modal.style.display = 'block';
   document.getElementById('my-table').style.display = "none"
   document.getElementById('nom_noeud_2').value = nom_noeud;
   document.getElementById('id_noeud').value = id_noeud;
   document.getElementById('puissance').value = puissances.join(', ');
}



    

	var btns = document.querySelectorAll(".btn-ho");
	console.log(btns)
    Array.from(btns).forEach(item => {
       item.addEventListener("click", () => {
		  console.log("click2");
		  console.log(item);
		  console.log(item.classList);
		  var selected = document.getElementsByClassName('activated');
		  console.log(selected[0].className);
		  selected[0].className = selected[0].className.replace(" activated", "");
          item.className += " activated";		  
		  
	   if (item.classList.contains('activated')) {		   
		   item.classList.add('activated');
		   console.log("It does TRUE")	   
	   } else { 
	       item.classList.add('activated');
	       console.log("Does NOT is FALSE") 
	   
	     };	  
 
       });
    });	
		

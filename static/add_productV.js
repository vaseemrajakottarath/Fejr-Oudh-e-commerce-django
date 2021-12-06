$(document).ready(()=>{
    $("#myform").validate({
        rules:{
            product_name:{
                required:true,
               
            },
           product_description:{
                required:true,
                
            },
          price:{
                required:true,
              
            },   
           stock:{
                required:true,
               
            },
        }
        })
    })
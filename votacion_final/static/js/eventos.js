var ventanamensaje=()=>{
  event.preventDefault();
  if(!document.querySelector('input[name="candidato"]:checked')) {
      Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Seleccione un candidato!',
        })
          hasError = true;
          }else{
      swal({
          title: "Estas seguro?",
          text: "Si estas de acuerdo presiona ok",
          icon: "warning",
          buttons: true,
          
       })
        .then((aceptar) => {
          if (aceptar) {
            Swal.fire({
              icon: 'success',
              title: 'Voto correcto',
              timer: 2000,
              showCancelButton: false,
              showConfirmButton: false,
              allowOutsideClick: false
              
            }, 
         )
          $.ajax({
          url:'/captar_voto', 
          data:$('form').serialize(),
          type:'POST',
          success: function(response){
          },
          error: function(error){
          }
          })
         window.setTimeout(function irindex(){
          location.href="../Inicio"}, 0800);
          } else {
           
          }
        });
      }
   }
    
var actualizar=()=>{
  event.preventDefault();
 
      swal({
        title: "Estas seguro?",
        text: "Si estas de acuerdo presiona ok",
        icon: "warning",
        buttons: true,
        
     })
      .then((aceptar) => {
        if (aceptar) {
        
          $.ajax({
            url:'/actualizar', 
            data:$('form').serialize(),
            type:'POST',
            success: function(response){
                
            },
            error: function(error){
                alert("Error")
            }
        })
        swal({
          title: "Actualizado Correctamente",
          type: "success",
          showConfirmButton: true
        })
        } else {
         
        }
      });
    }

var Reiniciarcandidatos=(ruta)=>{
      event.preventDefault();
     
          swal({
            title: "Estas seguro?",
            text: "Si estas de acuerdo presiona ok",
            icon: "warning",
            buttons: true,
            
         })
          .then((aceptar) => {
            if (aceptar) {
              $.ajax({
                url: ruta, 
                type:'GET',
                success: function(response){
                },
                error: function(error){
                    alert("Error")
                }
            })
            swal({
              title: "Reiniciado correctamente",
              type: "success",
              showConfirmButton: true
            })
            } else {
             
            }
          });
        }
var iniciarreloj=()=>{
  let fecha = document.getElementById("fecha").value
  let horas = document.getElementById("horas").value
  let minutos = document.getElementById("minutos").value
  let segundos = document.getElementById("segundos").value
  if(fecha != "" && horas!= "" && minutos != "" && segundos != ""  ){

    event.preventDefault();
         
    swal({
      title: "Estas seguro?",
      text: "Si estas de acuerdo presiona ok",
      icon: "warning",
      buttons: true,
      
   })
    .then((aceptar) => {
      if (aceptar) {
        $.ajax({
          url: '/actualizarreloj', 
          data:$('form').serialize(),
          type:'POST',
          
          success: function(response){
          },
          error: function(error){
              alert("Error")
          }
      })
      swal({
        title: "¡Fecha modificada exitosamente!",
        type: "success",
        showConfirmButton: true
      })
      } else {
       
      }
    });
  }

}

var iniciarreloj2=()=>{
  let fecha = document.getElementById("fecha2").value
  let horas = document.getElementById("horas2").value
  let minutos = document.getElementById("minutos2").value
  let segundos = document.getElementById("segundos2").value
  if(fecha != "" && horas!= "" && minutos != "" && segundos != ""  ){

    event.preventDefault();
         
    swal({
      title: "Estas seguro?",
      text: "Si estas de acuerdo presiona ok",
      icon: "warning",
      buttons: true,
      
   })
    .then((aceptar) => {
      if (aceptar) {
        $.ajax({
          url: '/actualizarrelojfin', 
          data:$('form').serialize(),
          type:'POST',
          
          success: function(response){
          },
          error: function(error){
              alert("Error")
          }
      })
      swal({
        title: "¡Fecha modificada exitosamente!",
        type: "success",
        showConfirmButton: true
      })
      } else {
       
      }
    });
  }

}


var eliminar_candidato=()=>{
    event.preventDefault();     
    swal({
      title: "Estas seguro?",
      text: "Si estas de acuerdo presiona ok",
      icon: "warning",
      buttons: true,      
   })
    .then((aceptar) => {
      if (aceptar) {
        $.ajax({
          url: '/eliminar_candidato', 
          data:$('form').serialize(),
          type:'POST',
          
          success: function(response){
          },
          error: function(error){
              alert("Error")
          }
          
      })
      swal({
        title: "¡Candidato eliminado correctamente!",
        type: "success",
        showConfirmButton: true
      })
      location.href="../eliminar_candidatos"
      } else {
       
      }
    });
}

var eliminar_mensaje=()=>{
  event.preventDefault();     
  swal({
    title: "Estas seguro?",
    text: "Si estas de acuerdo presiona ok",
    icon: "warning",
    buttons: true,      
 })
  .then((aceptar) => {
    if (aceptar) {
      $.ajax({
        url: '/eliminar_mensaje', 
        data:$('form').serialize(),
        type:'POST',
        
        success: function(response){
        },
        error: function(error){
            alert("Error")
        }
        
    })
    swal({
      title: "¡Mensaje eliminado correctamente!",
      type: "success",
      showConfirmButton: true
    })
    location.href="../contacto"
    } else {
     
    }
  });
}


var politicaseguridad=()=>{
  
  document.formulario.checkbox.click();
  swal({
    title: "Politica de datos personales",
    text: "Ley de Protección de Datos Personales o Ley 1581 de 2012 \n\nReconoce y protege el derecho que tienen todas las personas a conocer, actualizar y rectificar las informaciones que se hayan recogido sobre ellas en bases de datos o archivos que sean susceptibles de tratamiento por entidades de naturaleza pública o privada.",
    icon: "warning",
    buttons: true,      
 })
  .then((aceptar) => {
    if (aceptar) {
      
      for (let i=0; i < document.formulario.elements.length; i++) {
        if(document.formulario.elements[i].type === "checkbox") {
            document.formulario.elements[i].checked = true;
        }
    }
     
    } else {
      for (let i=0; i < document.formulario.elements.length; i++) {
        if(document.formulario.elements[i].type === "checkbox") {
            document.formulario.elements[i].checked = false;
        }
    }
    }
  });
 
}

    
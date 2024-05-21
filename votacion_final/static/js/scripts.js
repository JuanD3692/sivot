jQuery(function($){

'use strict';


    /* ---------------------------------------------- /*
     * CONTADOR
    /* ---------------------------------------------- */
   

    

    (function () {
      // Countdown
    	// PARA EDITAR LA FECHA HASTA DONDE VA A LLEGAR EL CONTADOR EDITAR LA VAR endDate;
    
    	$(function() {
       
       
        
        if (fechaactual > fechacomenzar && fechaterminar > fechaactual){
          
          tiempo = fechaf
          document.getElementById("mensaje1").textContent="Para terminar las votaciones"
          document.getElementById("mensaje").textContent="Inicia sesión para votar"
         
        }else if (fechaactual < fechacomenzar){
          
          document.getElementById("mensaje").textContent="Las votaciones comenzarán cuando termine el contador"
          tiempo = endDate
 

        }else{
         
          tiempo = output
          document.getElementById("mensaje1").textContent="Han terminado las votaciones"
          document.getElementById("mensaje2").textContent=""
          document.getElementById("mensaje").textContent="Las votaciones han terminado"
          document.getElementById("mensaje").addClass="text-white"
        }
     
    	  $('.tk-countdown .row').countdown({
       
    		date: tiempo,
        
    		render: function(data) {
          
    		  $(this.el).html('<div><div class="days"><span>' + this.leadingZeros(data.days, 2) + '</span><span>Días</span></div><div class="hours"><span>' + this.leadingZeros(data.hours, 2) + '</span><span>Horas</span></div></div><div class="tk-countdown-ms"><div class="minutes"><span>' + this.leadingZeros(data.min, 2) + '</span><span>Minutos</span></div><div class="seconds"><span>' + this.leadingZeros(data.sec, 2) + '</span><span>Segundos</span></div></div>');
    		}
        
    	  });
       
    	});	
     
    }());


    /* ---------------------------------------------- /*
     * FOTO DE PRE CARGA
    /* ---------------------------------------------- */
    
    (function () {
        $(window).load(function() {
            $('#pre-status').fadeOut();
            $('#st-preloader').delay(350).fadeOut('slow');
        });
    }());



    /* ---------------------------------------------- /*
     * Ajax Forms
    /* ---------------------------------------------- */

    (function () {
        // E-mail validation via regular expression
        function isValidEmailAddress(emailAddress) {
          var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
          return pattern.test(emailAddress);
        };

    	// Ajax mailchimp
        // Example MailChimp url: http://xxx.xxx.list-manage.com/subscribe/post?u=xxx&id=xxx
        $('#subscribe').ajaxChimp({
          language: 'es',
          url: 'http://xxx.xxx.list-manage.com/subscribe/post?u=xxx&id=xxx'
        });

        // Mailchimp translation
        //
        // Defaults:
        //'submit': 'Submitting...',
        //  0: 'We have sent you a confirmation email',
        //  1: 'Please enter a value',
        //  2: 'An email address must contain a single @',
        //  3: 'The domain portion of the email address is invalid (the portion after the @: )',
        //  4: 'The username portion of the email address is invalid (the portion before the @: )',
        //  5: 'This email address looks fake or invalid. Please enter a real email address'

        $.ajaxChimp.translations.es = {
          'submit': 'Submitting...',
          0: '<i class="fa fa-check"></i> We will be in touch soon!',
          1: '<i class="fa fa-warning"></i> You must enter a valid e-mail address.',
          2: '<i class="fa fa-warning"></i> E-mail address is not valid.',
          3: '<i class="fa fa-warning"></i> E-mail address is not valid.',
          4: '<i class="fa fa-warning"></i> E-mail address is not valid.',
          5: '<i class="fa fa-warning"></i> E-mail address is not valid.'
        }

    }());

	
});

let date = new Date();
let output = date.getFullYear() + '-' + String(date.getMonth() + 1).padStart(2, '0') + '-' + String(date.getDate()).padStart(2, '0') +" "+ String(date.getHours())+":"+ String(date.getUTCMinutes())+":"+String(date.getUTCSeconds());
let endDate =  document.getElementById("comenzar").value
let fechaf =  document.getElementById("terminar").value
let tiempo=0

let fechacomenzar= new Date(endDate) 
let fechaterminar =new Date(fechaf) 
let fechaactual =new Date(output) 



var verrestultados=()=>{
  if (fechaactual > fechacomenzar && fechaterminar > fechaactual){
    location.href="/resultados"
  }else if (fechaactual < fechacomenzar){
      Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Aún no comienzan las elecciones',
    })
   
  }else{
    location.href="/resultados"
  }

}

var registrarse=()=>{
  if (fechaactual > fechacomenzar && fechaterminar > fechaactual){
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'No puedes registrarte mientras las elecciones estén en curso',
    })
  }else{

    location.href="/registrar_user"

}
}
var votar=()=>{
  
 
    if (fechaactual > fechacomenzar && fechaterminar > fechaactual){ 

    }else if (fechaactual < fechacomenzar){
      event.preventDefault();
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'No puedes votar si las votaciones no han comenzado',
      }) 
    }else{
      event.preventDefault();
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Las votaciones ya terminaron',
      }) 
    }
   }
  


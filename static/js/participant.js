var elem = document.querySelector('select');
var instance = M.FormSelect.init(elem, options);

  // Or with jQuery

$(document).ready(function(){
  $('select').formSelect();
});
$(document).ready(function() {
    $('select').material_select();
});
var instance = M.FormSelect.getInstance(elem);

  /* jQuery Method Calls
    You can still use the old jQuery plugin method calls.
    But you won't be able to access instance properties.

    $('select').formSelect('methodName');
    $('select').formSelect('methodName', paramName);
  */
instance.getSelectedValues();
instance.destroy();
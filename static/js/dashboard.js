$(".Navigation-list-item").on("click", function() {
  $(".Navigation-list-item").removeClass("active");
  $(this).addClass("active");
});

$('.pins').masonry({
  // options
  itemSelector: '.pin',
  columnWidth: 400,
  fitWidth: true,
  transitionDuration: '0.2s'
});

function switchbuttons(buttonId) {
  var hideBtn, showBtn, menuToggle, steps_id;
  if (buttonId == 'button1') {
    steps_id = 'step1';
    showBtn = 'button2';
    hideBtn = 'button1';
  } else if (buttonId =='button2'){
    menuToggle = 'menu3';
    steps_id = 'step2';
    showBtn = 'button3';
    hideBtn = 'button2';
  }else if (buttonId =='button3'){
    steps_id = 'step3';
    showBtn = 'button4';
    hideBtn = 'button3';
  }else {
    hideBtn = 'button4';
    steps_id = 'step4';
  }
  //I don't have your menus, so this is commented out.  just uncomment for your usage
  // document.getElementById(menuToggle).toggle(); //step 1: toggle menu
  document.getElementById(hideBtn).style.display = 'none'; //step 2 :additional feature hide button
  document.getElementById(showBtn).style.display = 'block'; //step 3:additional feature show button
  document.getElementById(steps_id).className = 'active';
}

/*
* This is the plugin
*/
(function(a){a.createModal=function(b){defaults={title:"",message:"Your Message Goes Here!",closeButton:true,scrollable:false};var b=a.extend({},defaults,b);var c=(b.scrollable===true)?'style="max-height: 420px;overflow-y: auto;"':"";html='<div class="modal fade" id="myModal">';html+='<div class="modal-dialog">';html+='<div class="modal-content">';html+='<div class="modal-header">';html+='<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>';if(b.title.length>0){html+='<h4 class="modal-title">'+b.title+"</h4>"}html+="</div>";html+='<div class="modal-body" '+c+">";html+=b.message;html+="</div>";html+='<div class="modal-footer">';if(b.closeButton===true){html+='<button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>'}html+="</div>";html+="</div>";html+="</div>";html+="</div>";a("body").prepend(html);a("#myModal").modal().on("hidden.bs.modal",function(){a(this).remove()})}})(jQuery);

/*
* Here is how you use it
*/
$(function(){
    $('.view-pdf').on('click',function(){
        var pdf_link = $(this).attr('href');
        var iframe = '<div class="iframe-container"><iframe src="'+pdf_link+'"></iframe></div>'
        $.createModal({
        title:'My Title',
        message: iframe,
        closeButton:true,
        scrollable:false
        });
        return false;
    });
})
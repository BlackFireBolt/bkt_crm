$('#add-lead-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted");
    $('#addLeadModal').modal('toggle');
    var url = "/add-lead/";
    create_lead(url);
});

$('#change-lead-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted");
    var lead_id = $('#lead_change').data("id"),
        url = "/change-lead/";
    create_lead(url, lead_id);
});

var UpdateLead = function(from, align, id){
    	color = Math.floor((Math.random() * 4) + 1);

    	$.notify({
        	icon: "tim-icons icon-bell-55",
        	message: "Лид номер " + id + " обновлен."

        },{
            type: type[color],
            timer: 8000,
            placement: {
                from: from,
                align: align
            }
        });
	}

function create_lead(url, lead_id=null){
    $.ajax({
        url: url,
        type: "POST",
        data: {
            leadpk: lead_id,
            name: $('#post_name').val(),
            email: $('#post_email').val(),
            phone: $('#post_phone').val(),
            country: $('#post_country').val(),
            created_date: $('#post_created_date').val(),
            manager: $('#post_manager').val(),

            notes: $('#post_notes').val(),
            status: $('#post_status').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
              },
        success:function(json){
            console.log("success");
            if (json.flag == 'change'){
                UpdateLead('top', 'left', lead_id);
            }
        },
        error:function(xhr,errmsg,err) {
            console.log("error");
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
};
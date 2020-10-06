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

var ErrorLead = function(from, align, id){
    	color = Math.floor((Math.random() * 4) + 1);

    	$.notify({
        	icon: "tim-icons icon-bell-55",
        	message: " При обновлении лида номер " + id + " обнаружена ошибка."

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
            time_zone: $('#post_time_zone').val(),
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
            } else if (json.flag == 'error'){
                ErrorLead('top', 'left', lead_id);
            }
        },
        error:function(xhr,errmsg,err) {
            console.log("error");
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
};

$('#add_import').submit(function(event) {
    event.preventDefault();
    $form = $(this)
    var formData = new FormData(this);
    $.ajax({
        url: "/import_csv/",
        type: 'POST',
        data: formData,
        success: function (response){},
        error: function(response){}
    });
});

$('#add_manager').click(function(event){
    event.preventDefault();
        $('#addManagerModal').modal('toggle');
    var table = $('.datatable').DataTable();
    var tblData = table.rows( { selected: true } ).data();
    var tmpData = [];
    for (var i=0; i < tblData.length; i++) {
        tmpData.push(tblData[i].id);
    };
    $.ajax({
        url: "/add_manager/",
        type: 'POST',
        data: {
            manager: $('#post_inner_manager').val(),
            data: tmpData,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response){
            location.reload();
        },
        error: function(response){}
    });
});

$('#add-lead-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted");
    $('#addLeadModal').modal('toggle');
    var url = "/add-lead/";
    create_lead(url);
});

$('#lead_change').click(function(event){
    event.preventDefault();
    console.log("form submitted");
    var lead_id = $('#lead_change').data("id"),
        url = "/change-lead/";
    create_lead(url, lead_id);
});

var UpdateLead = function(from, align, id){
    	$.notify({
        	icon: "tim-icons icon-bell-55",
        	message: "Лид номер " + id + " обновлен."

        },{
            type: 'info',
            timer: 0,
            placement: {
                from: from,
                align: align
            }
        });
	}

var ErrorLead = function(from, align, id){
    	$.notify({
        	icon: "tim-icons icon-bell-55",
        	message: " При обновлении лида номер " + id + " обнаружена ошибка."

        },{
            type: 'danger',
            timer: 0,
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
            depozit: $('#post_depozit').val(),
            phone: $('#post_phone').val(),
            country: $('#post_country').val(),
            time_zone: $('#post_time_zone').val(),
            created_date: $('#post_created_date').val(),
            manager: $('#post_manager').val(),

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
            var data = json.content;
            var table = $('.datatable').DataTable();
            var rowNode = table.row.add(data).draw().node();
            $(rowNode).css('color', 'red').animate({color: 'black'});
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

$('#add_note').click(function (event){
    event.preventDefault();
    var lead_id = $('#add_note').data("id");
    console.log(post_note);
    $.ajax({
        url:"/add-note/",
        type:"POST",
        data:{
            lead_id: lead_id,
            note_data: post_note = $('#post_note').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success:function(json){
            $('#post_note').val('');
            $('<div class="card">' + '<div class="card-body">' + '<p class="mb-auto">' + json.note_created_date + '</p>' + '<p class="mb-auto">' + json.note_text +'</p>' +
                '</div>' + '</div>').hide().appendTo('.notes').show('slow');
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },
        error : function(xhr,errmsg,err) {
            console.log("error");
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});

$('#add_notification').click(function (event){
    event.preventDefault();
    var lead_id = $('#add_notification').data("id");
    $.ajax({
        url:"/add-notification/",
        type:"POST",
        data:{
            lead_id: lead_id,
            notification_data: $('#post_notification').val(),
            time: $('#post_time').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success:function(json){
            $('#post_notification').val('');
            $('#post_time').val('');
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },
        error : function(xhr,errmsg,err) {
            console.log("error");
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});

$('.side-content').on('click', '.task-button', function(event){
    event.preventDefault();
    var task_id = $(this).data('id');
    $.ajax({
        url:"/update-task/",
        type:"POST",
        data:{
            task_id: task_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success:function(json){
            console.log("success"); // another sanity check
        },
        error : function(xhr,errmsg,err) {
            console.log("error");
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});

$('#add_task').click(function (event){
    event.preventDefault();
    $('#addTaskModal').modal('toggle');
    $.ajax({
        url:"/add-task/",
        type:"POST",
        data:{
            manager: $('#task_manager').val(),
            text: $('#task_text').val(),
            expiration_time: $('#task_expiration_time').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success:function(json){
            $('#task_manager').val('');
            $('#task_text').val('');
            $('#task_expiration_time').val('');
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },
        error : function(xhr,errmsg,err) {
            console.log("error");
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});
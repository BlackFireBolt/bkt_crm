    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var ws_path = ws_scheme + '://' + window.location.host + "/ws/ticks/";
            console.log("Connecting to " + ws_path);
            var socket = new ReconnectingWebSocket(ws_path);

    var NewLead = function(from, align){
    	$.notify({
        	icon: "tim-icons icon-bell-55",
        	message: "Добавлен новый лид."

        },{
            type: 'info',
            timer: 0,
            placement: {
                from: from,
                align: align
            }
        });
	}
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
	var NotifyLead = function(from, align, lead, text){
    	$.notify({
        	icon: "tim-icons icon-bell-55",
        	message: "Лид номер " + lead + ", напоминание: " + text,

        },{
            type: 'warning',
            timer: 0,
            placement: {
                from: from,
                align: align
            }
        });
	}
    socket.onmessage = function(event) {
        var data = JSON.parse(event.data);
        console.log(data)
        if (data.type == 'data.notification'){
            console.log('task notif', data);
            NotifyLead('top', 'left', data.lead, data.text);
	        var options = {
	            title: "BKT crm",
	            options: {
	            body: "Лид номер " + data.lead + ", напоминание: \n" + data.text,
	            icon: "https://bkt-crm.tk/static/assets/img/favicon.ico",
	            lang: 'ru-RU',
	            }
	        };
	        $("#easyNotify").easyNotify(options);
        } else if (data.type == 'task.new') {
            if (data.task_type == 'n') {
            $('<div class="card" id="task-' + data.id + '">' + '<div class="card-body">' + '<h4 class="card-title" id="task-' + data.id + '-title">' +
            data.expiration_time + '</h4>' + '<h6 class="card-subtitle mb-2 text-muted">Лид №' + data.lead + '</h6><span class="badge badge-warning mb-2">Напоминание</span>'
            + '<p class="card-text" id="task-' + data.id + '-text">' + data.text +'</p>' + '<p>Менеджер: ' + data.manager +'</p>' + '<button id="task-' + data.id
            + '-button" class="task-button btn btn-fab btn-icon btn-round animation-on-hover float-right" type="button"'
             + 'data-id="' + data.id + '">' +
            '<i class="tim-icons icon-check-2"></i>' + '</button>' + '</div>' + '</div>')
            .hide().prependTo('.side-content').show('slow');
            } else if (data.task_type == 't'){
            $('<div class="card" id="task-' + data.id + '">' + '<div class="card-body">' + '<h4 class="card-title" id="task-' + data.id + '-title">' +
            data.expiration_time + '</h4>' + '<span class="badge badge-info mb-2">Задача</span>' + '<p class="card-text" id="task-' + data.id + '-text">' + data.text +'</p>'
            + '<p>Менеджер: ' + data.manager +'</p>' + '<button id="task-' + data.id
            + '-button" class="task-button btn btn-fab btn-icon btn-round animation-on-hover float-right" type="button"'
             + 'data-id="' + data.id + '">' +
            '<i class="tim-icons icon-check-2"></i>' + '</button>' + '</div>' + '</div>')
            .hide().prependTo('.side-content').show('slow');
            }
        } else if (data.type == 'task.update') {
            if (!data.complete) {
                var task_id = '#task-' + data.id,
                    task_button = task_id + '-button';
                $(task_id).addClass('bg-danger');
                console.log(task_id, task_button);
                $(task_button).attr('disabled', 'true');
            } else {
                var task_id = data.id;
                $('#task-' + task_id).fadeOut('slow');
            }
        } else  {
            var table = $('.datatable').DataTable();
            var rowNode = table.row.add(data).draw().node();
            console.log('id', table.rows({selected: true}).data('id'));
            $(rowNode).css('color', 'red').animate({color: 'black'});
            if (data.type == 'data.new') {
                NewLead('top', 'left');
            } else if (data.type == 'data.update') {
                        UpdateLead('top', 'left', data.id);
                    }
            }
    };

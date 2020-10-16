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

        var table = $('.datatable').DataTable();

        if (data.type == 'data.notification'){
            console.log('task', data);
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
        }
        else {
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

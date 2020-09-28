    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var ws_path = ws_scheme + '://' + window.location.host + "/ws/ticks/";
            console.log("Connecting to " + ws_path);
            var socket = new ReconnectingWebSocket(ws_path);

    var NewLead = function(from, align){
    	color = Math.floor((Math.random() * 4) + 1);

    	$.notify({
        	icon: "tim-icons icon-bell-55",
        	message: "Добавлен новый лид."

        },{
            type: type[color],
            timer: 8000,
            placement: {
                from: from,
                align: align
            }
        });
	}
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
    socket.onmessage = function(event) {
        var data = JSON.parse(event.data);
        console.log('data', data);
        var table = $('.datatable').DataTable();
        console.log('id', data.id);
        console.log('id', data['id']);

        var rowNode = table.row.add(data).draw().node();
        $(rowNode).css('color', 'red').animate({color: 'black'});
        if (data.type == 'data.new') {
        NewLead('top', 'left');
        } else if (data.type == 'data.update') {
        UpdateLead('top', 'left', data.id);
        }
    };

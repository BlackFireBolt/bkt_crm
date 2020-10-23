$(document).ready(function() {
var dt_table = $('.datatable').dataTable({
        language: dt_language,  // global variable defined in html
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        order: [[ 0, "desc" ]],
        searching: true,
        columnDefs: [
            {
                data: 'id',
                targets: [0],
                orderable: true,
            },
            {
                data: 'status',
                targets: [1],
                orderable: true,
            },
            {
                data: 'name',
                targets: [2],
                orderable: true,
            },
            {
                data: 'phone',
                targets: [3],
                orderable: true,
            },
            {
                data: 'country',
                targets: [4],
                orderable: true,
            },
            {
                data: 'depozit',
                targets: [5],
                orderable: true,
            },
            {
                data: 'created_date',
                targets: [6],
                orderable: true,
            },
        ],
        processing: true,
        serverSide: true,
        stateSave: true,
        createdRow: function( row, data, dataIndex ) {
                             switch($(data['status']).text()){
                                    case 'Новый':
                                            $("td:eq(0)",row).addClass('table_new');
                                            break;
                                    case 'Аут':
                                            $("td:eq(0)",row).addClass('table_aut');
                                            break;
                                    case 'Не интересно':
                                            $("td:eq(0)",row).addClass('table_notinteres');
                                            break;
                                    case 'Потенциал':
                                            $("td:eq(0)",row).addClass('table_potential');
                                            break;
                                    case 'Не отвечает':
                                            $("td:eq(0)",row).addClass('table_na');
                                            break;
                                    case 'Клиент':
                                            $("td:eq(0)",row).addClass('table_client');
                                            break;
                                    case 'Горячий':
                                            $("td:eq(0)",row).addClass('table_hot');
                                            break;
                            }
        },
        ajax: LIST_JSON_URL
    });
    });